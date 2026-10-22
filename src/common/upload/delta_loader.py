from airflow.models import BaseOperator

from common.helper.upload_helper import LoadTableHelper

class DeltaLoaderOperator(BaseOperator):

    template_fields = ('sql_query', 'value_day', 'job_id') #'source_schema', 'source_table', 'target_schema', 'target_table', 'as_of_day'

    template_ext = ('.sql',)

    def __init__(
        self,
        p_hook,
        # p_dag_name,
        p_job_id,
        p_source_schema,
        p_source_table,
        p_target_schema,
        p_target_table,
        p_sql_query,
        p_value_day,
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
        self.sql_query = p_sql_query
        self.value_day = p_value_day
        self.as_of_day = p_as_of_day
        self.drop_duplicates = p_drop_duplicates
        self.gather_stats = p_gather_stats

    def execute(self, context):
        helper = LoadTableHelper(123, 123, 123)

        if self.drop_duplicates:
            self.log.info('Start drop_duplicates()')
            helper.drop_duplicates()
            self.log.info('End drop_duplicates()')

        # main logic
        self.log.info(f'Starting {self.target_schema}.{self.target_table} table loading')

        formatted_sql = self.sql_query.format(self=self)

        self.hook.run(sql=formatted_sql)

        if self.gather_stats:
            self.log.info(f'Start gathering stats for {self.target_schema}.{self.target_table}')
            helper.gather_table_stats()
            self.log.info('End gathering stats')