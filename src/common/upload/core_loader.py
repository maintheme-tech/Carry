from airflow.models import BaseOperator

from common.helper.upload_helper import LoadTableHelper

class LoadCoreTableOperator(BaseOperator):

    # template_fields = (,)

    def __init__(
        self,
        p_hook,
        p_source_schema,
        p_source_table,
        p_target_schema,
        p_target_table,
        p_as_of_day,
        p_drop_duplicates,
        p_gather_stats,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.hook = p_hook
        self.source_schema = p_source_schema
        self.source_table = p_source_table
        self.target_schema = p_target_schema
        self.target_table = p_target_table
        self.as_of_day = p_as_of_day
        self.drop_duplicates = p_drop_duplicates
        self.gather_stats = p_gather_stats

    def execute(self, context):
        helper = LoadTableHelper(
            p_hook=self.hook,
            p_source_schema=self.source_schema,
            p_source_table=self.source_table,
            p_target_schema=self.target_schema,
            p_target_table=self.target_table,
            p_as_of_day=self.as_of_day
        )

        if helper.check_empty_source():
            self.log.warning(f'Source table {self.source_schema}.{self.source_table} is empty!')
            return 

        if self.drop_duplicates:
            self.log.info('Start drop_duplicates()')
            helper.drop_duplicates()
            self.log.info('End drop_duplicates()')

        self.log.info('Generating merge statement')
        merge_statement = helper.generate_merge_statement(self.as_of_day)

        self.hook.run(sql=merge_statement)