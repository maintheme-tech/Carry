
class LoadTableHelper:
    
    def __init__(
        self,
        p_hook,
        p_schema_name,
        p_table_name
    ):
        self.hook = p_hook
        self.schema_name = p_schema_name
        self.table_name = p_table_name

    def drop_duplicates(self):
        return self.hook + self.schema_name

    def get_table_constraints(self):
        return ...

    def gather_table_stats(self):
        return ...