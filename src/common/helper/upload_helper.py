import logging


class LoadTableHelper:
    
    def __init__(
        self,
        p_hook,
        p_source_schema,
        p_source_table,
        p_target_schema,
        p_target_table,
        p_as_of_day
    ):
        self.hook = p_hook
        self.source_schema = p_source_schema
        self.source_table = p_source_table
        self.target_schema = p_target_schema
        self.target_table = p_target_table
        self.as_of_day = p_as_of_day
        self.logger = logging.getLogger(__name__)


    def drop_source_duplicates(self):
        columns_metadata = self.get_columns_metadata()

        target_keys = [d['column_name'] for d in columns_metadata if d['primary_key_flag']]
        merge_condition = "\n            AND ".join(
            f"target.{column_name} = source.{column_name}"
            for column_name in target_keys
        )
        target_keys = ", ".join(target_keys)

        self.logger.info(f'Obtained Source table keys: {target_keys}')

        self.hook.run(sql=f'''
        MERGE INTO {self.source_schema}.{self.source_table} AS target
        USING (
            SELECT {target_keys},
                ROW_NUMBER() OVER (PARTITION BY {target_keys}) AS rn
            FROM {self.source_schema}.{self.source_table}
        ) AS source
        ON {merge_condition}
        AND source.rn > 1
        WHEN MATCHED THEN DELETE
        ''')

        self.hook.log_sql = True

    def gather_table_stats(self):
        self.hook.run(sql=f'''
            analyze {self.target_schema}.{self.target_table}
        ''')

    def check_empty_source(self):
        
        self.hook.log_sql = False
        count = self.hook.get_first(sql=f'''
            select count(*)
            from {self.source_schema}.{self.source_table}
        ''')
        self.hook.log_sql = True

        return count[0] == 0


    def get_columns_metadata(self):

        columns = ["column_name", "primary_key_flag", "on_match_update_flag"]
        
        self.hook.log_sql = False
        records = (self.hook.get_records(f'''
            select {", ".join(columns)}
            from iceberg.tables_metadata.md_columns 
            where 1=1
            and schema_name = '{self.target_schema}'
            and table_name = '{self.target_table}'
            and active_flag = True
            order by ordinal_position asc
        '''))
        self.hook.log_sql = True

        return [dict(zip(columns, record)) for record in records]
    
    def generate_merge_statement(self):

        columns_metadata = self.get_columns_metadata()

        target_keys = [d['column_name'] for d in columns_metadata if d['primary_key_flag']]
        update_fields = [d['column_name'] for d in columns_metadata if d['on_match_update_flag']]
        insert_fields = [d['column_name'] for d in columns_metadata]

        merge_condition = "\n            AND ".join(
            f"target.{column_name} = source.{column_name}"
            for column_name in target_keys
        )

        match_update = ",\n                     ".join(
            f"{column_name} = source.{column_name}"
            for column_name in update_fields
        )
        
        insert_values = ", ".join(
            f"source.{column_name}" if column_name != 'as_of_day' 
            else f"TIMESTAMP '{self.as_of_day}'"
            for column_name in insert_fields
        )

        merge_statement = f'''
            MERGE INTO {self.target_schema}.{self.target_table} AS target
            USING {self.source_schema}.{self.source_table} AS source
            ON {merge_condition}
            WHEN MATCHED 
                THEN UPDATE
                    SET {match_update}
            WHEN NOT MATCHED
                THEN INSERT ({", ".join(insert_fields)})
                    VALUES ({insert_values})
        '''

        return merge_statement


