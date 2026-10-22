from airflow.models import BaseOperator

from common.helper.upload_helper import LoadTableHelper

class LoadCoreTableOperator(BaseOperator):

    # template_fields = (,)

    # template_ext = ('.sql',)

    def __init__(
        self,
        p_hook,
        # p_dag_name,
        p_job_id,
        p_source_schema,
        p_source_table,
        p_target_schema,
        p_target_table,
        # p_sql_query,
        p_as_of_day,
        p_drop_duplicates,
        p_gather_stats,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.hook = p_hook
        # self.dag_name = p_dag_name
        self.job_id = p_job_id
        self.source_schema = p_source_schema
        self.source_table = p_source_table
        self.target_schema = p_target_schema
        self.target_table = p_target_table
        # self.sql_query = p_sql_query
        self.as_of_day = p_as_of_day
        self.drop_duplicates = p_drop_duplicates
        self.gather_stats = p_gather_stats

    def execute(self, context):
        helper = LoadTableHelper(...)

        if helper.check_empty_source(self.source_schema, self.source_table):
            self.log.warning(f'Source table {self.source_schema}.{self.source_table} is empty!')
            return 

        if self.drop_duplicates:
            self.log.info('Start drop_duplicates()')
            helper.drop_duplicates()
            self.log.info('End drop_duplicates()')
    
        primary_key_attributes, attributes_to_update, attributes_to_insert = helper.collect_table_attributes_info(self.target_schema, self.target_table)

        self.log.info(f'Obtained table\'s key: {*primary_key_attributes}')

        self.log.info('Generating merge statement')
        merge_statement = helper.generate_merge_statement(
                                self.source_schema, self.source_table,
                                self.target_schema, self.target_table,
                                composite_key_attributes,
                                attributes_to_update,
                                attributes_to_insert,
                                self.job_id
                            )

        self.hook.run(sql=merge_statement)