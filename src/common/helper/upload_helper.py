
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
        return ...

    def get_table_constraints(self):
        return ...

    def gather_table_stats(self):
        return ...

    def check_empty_source(self, schema_name, table_name):
        return ...

    def collect_table_attributes_info(self):
        return ...
    
    def generate_merge_statement(self):
        return ...
