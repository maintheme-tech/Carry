from airflow.models import BaseOperator


class RunSQLQueryOperator(BaseOperator):

    template_fields = ('sql_query_path',)

    template_ext = ('.sql',)

    def __init__(
        self,
        p_sql_query_path,
        p_hook,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.sql_query_path = p_sql_query_path
        self.hook = p_hook

    def execute(self, context):

        self.hook.run(sql=self.sql_query_path)