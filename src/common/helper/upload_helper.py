
class LoadTableHelper:
    
    def __init__(
        self,
        p_hook,
        p_schema_name,
        p_table_name
    ):
        self.hook = p_hook
        self.source_schema = p_source_schema
        self.source_table = p_source_table
        self.target_schema = p_target_schema
        self.target_table = p_target_table


    def drop_duplicates(self):
        return ...

    def get_table_constraints(self):
        return ...

    def gather_table_stats(self):
        return ...

    def check_empty_source(self, schema_name, table_name):
        return ...

    def get_columns_metadata(self):

        columns = ["column_name", "primary_key_flag", "on_match_update_flag"]

        records = (self.hook.get_records(f'''
            select {", ".join(columns)}
            from iceberg.tables_metadata.md_columns 
            where 1=1
            and schema_name = '{self.target_schema}'
            and table_name = '{self.target_table}'
            and active_flag = True
            order by ordinal_position asc
        '''))

        return [dict(zip(columns, record)) for record in records]
    
    def generate_merge_statement(self):

        columns_metadata = get_columns_metadata()

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
            f"source.{column_name}"
            for column_name in insert_fields
        )

        merge_statement = f'''
            merge into {self.target_schema}.{self.target_table} as target
            using {self.source_schema}.{source_table} as source
            on {merge_condition}
            when matched 
                then update
                    set {match_update}
            when not matched 
                then insert ({", ".join(insert_fields)})
                    values ({insert_values})
        '''

        return merge_statement
