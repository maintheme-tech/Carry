import logging

from common.helper.upload_helper import LoadTableHelper

class LoadHistTableOperator(BaseOperator):
    
    # template_fields = (,)

    def __init__(
        self,
        p_hook,
        p_source_schema,
        p_source_table,
        p_target_schema,
        p_target_table,
        p_as_of_day,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.hook = p_hook,
        self.source_schema = p_source_schema
        self.source_table = p_source_table
        self.target_schema = p_target_schema
        self.target_table = p_target_table
        self.as_of_day = p_as_of_day

    def execute(self):

        helper = LoadTableHelper(
            p_hook=self.hook,
            p_source_schema=self.source_schema,
            p_source_table=self.source_table,
            p_target_schema=self.target_schema,
            p_target_table=self.target_table,
            p_as_of_day=self.as_of_day
        )

        # step 1 obtain slice of new data


        # step 2 fetch current slice of open entries from hist table

        # step 3 define newly arrived data from new data and currently open entries

        # step 4 define entries that must be deleted (marked so) from hist table

        # step 5 define entries with updated attributes then cloase and reopen such rows

        # step 6 merge data from previous steps into target table