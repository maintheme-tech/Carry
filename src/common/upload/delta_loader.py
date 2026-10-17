import logging

from airflow.models import BaseOperator

from common.helper.upload_helper import LoadTableHelper

class DeltaLoaderOperator(BaseOperator):

    template_fields = ('sql_query',) #'source_schema', 'source_table', 'target_schema', 'target_table', 'as_of_day'

    template_ext = ('.sql',)

    def __init__(
        self,
        p_hook,
        # p_dag_name,
        # p_job_id,
        p_source_schema,
        p_source_table,
        p_target_schema,
        p_target_table,
        p_sql_query,
        p_as_of_day,
        p_drop_duplicates,
        p_gather_stats,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.hook = p_hook
        # self.dag_name = p_dag_name
        # self.job_id = p_job_id
        self.source_schema = p_source_schema
        self.source_table = p_source_table
        self.target_schema = p_target_schema
        self.target_table = p_target_table
        self.sql_query = p_sql_query
        self.as_of_day = p_as_of_day
        self.drop_duplicates = p_drop_duplicates
        self.gather_stats = p_gather_stats
        self.logger = logging.getLogger(__name__)

    def execute(self, context):
        delta_load_helper = LoadTableHelper(123, 123, 123)
        value_day = context['logical_date'].in_timezone('Europe/Moscow').subtract(days=1).to_date_string()

        if self.drop_duplicates:
            print('Start drop_duplicates()')
            delta_load_helper.drop_duplicates()
            print('End drop_duplicates()')

        # main logic
        print(f'Starting {self.target_schema}.{self.target_table} table loading')

        formatted_sql = self.sql_query.format(self=self, value_day=value_day)

        self.hook.run(sql=formatted_sql)

        if self.gather_stats:
            print(f'Start gathering stats for {self.target_schema}.{self.target_table}')
            delta_load_helper.gather_table_stats()
            print('End gathering stats')