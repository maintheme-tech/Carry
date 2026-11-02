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

        # step 1 obtain slice of fresh data

        ### Slice of new data is obtained from delta table

        # step 2 fetch current slice of open entries from hist table

        ### script_autoru_stg__proc_active_listings

        # step 3 define newly arrived data from new data and currently open entries

        ### script_autoru_stg_proc_new_listings

        # step 4 define entries that must be deleted (marked so) from hist table

        ### script_autoru_stg__proc_deleted_listings

        # step 5 define entries with updated attributes then close and reopen such rows

        # step 5.1
        # there are 2 steps in updating current data, firstly there are rows that will be inserted
        # during merge with updated attributes, new valid_from and 5999 valid_to
        #step 5.2
        # secondly, there are old records that will be updated in merge statement
        # so theirs valid_to becomes valid_from of a new updated row, meaning that raw is closed.

        ### script_autoru_stg__proc_updated_listings

        # step 6 merge data from previous steps into target table
        merge_statement = helper.generate_merge_statement(mode='hist')
        self.hook.run(sql=merge_statement)