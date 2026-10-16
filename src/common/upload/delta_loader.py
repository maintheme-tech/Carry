from airflow.models import BaseOperator

from common.helper.upload_helper import LoadTableHelper

class DeltaLoaderOperator(BaseOperator):

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

    def execute(self, context):
        delta_load_helper = LoadTableHelper(123, 123, 123)
        value_day = context['logical_date'].in_timezone('Europe/Moscow').subtract(days=1).to_date_string()

        print(self.as_of_day)
        print(value_day)

        if self.drop_duplicates:
            print('Start drop_duplicates()')
            delta_load_helper.drop_duplicates()
            print('End drop_duplicates()')

        # main logic
        print(f'Starting {self.target_schema}.{self.target_table} table loading')

        self.hook.run(sql=f"""
            truncate table {self.target_schema}.{self.target_table}
        """)

        print(f'Inserting data into {self.target_schema}.{self.target_table} for value_day={value_day}')

        self.hook.run(sql=f"""
            INSERT INTO {self.target_schema}.{self.target_table} (
                auto_ru_id,
                url,
                model_title,
                year,
                mileage,
                price,
                engine_volume,
                power_hp,
                power_kw,
                fuel,
                body_type,
                drive,
                transmission,
                sale_status,
                color,
                complectation,
                seller,
                seller_profile_url,
                seller_verified,
                seller_rating,
                seller_region,
                seller_address,
                photo_count,
                photo_urls,
                badges,
                value_day,
                as_of_day
            )
            SELECT
                TRY_CAST(auto_ru_id AS BIGINT) AS auto_ru_id,
                url,
                model_title,
                CAST(year AS INTEGER) AS year,
                mileage,
                price,
                -- engine_volume: Если в поле оказалась мощность (л.с./hp/кВт/kW) — NULL.
                CASE
                    WHEN engine_volume IS NULL OR TRIM(engine_volume) = '' THEN NULL
                    WHEN REGEXP_LIKE(LOWER(engine_volume), '(л\\.?с|hp|квт|kw)') THEN NULL
                    ELSE TRY_CAST(
                            REPLACE(
                                REGEXP_EXTRACT(engine_volume, '([0-9]+([.,][0-9]+)?)'),
                                ',', '.'
                            ) AS DOUBLE
                        )
                END AS engine_volume,
                -- power_hp: л.с. из power, а если там кВт — из engine_volume 
                CASE
                    WHEN power IS NOT NULL AND TRIM(power) <> ''
                        AND REGEXP_LIKE(LOWER(power), '(л\\.?с|hp)')
                        THEN TRIM(power)
                    WHEN engine_volume IS NOT NULL AND TRIM(engine_volume) <> ''
                        AND REGEXP_LIKE(LOWER(engine_volume), '(л\\.?с|hp)')
                        THEN TRIM(engine_volume)
                    ELSE NULL
                END AS power_hp,
                -- power_kw: кВт из power, а если там не кВт — из engine_volume (свап)
                CASE
                    WHEN power IS NOT NULL AND TRIM(power) <> ''
                        AND REGEXP_LIKE(LOWER(power), '(квт|kw)')
                        THEN TRIM(power)
                    WHEN engine_volume IS NOT NULL AND TRIM(engine_volume) <> ''
                        AND REGEXP_LIKE(LOWER(engine_volume), '(квт|kw)')
                        THEN TRIM(engine_volume)
                    ELSE NULL
                END AS power_kw,
                fuel,
                body_type,
                drive,
                transmission,
                sale_status,
                color,
                complectation,
                seller,
                seller_profile_url,
                seller_verified,
                seller_rating,
                seller_region,
                seller_address,
                CAST(photo_count AS INTEGER)  AS photo_count,
                photo_urls,
                badges,
                value_day,
                CAST('{self.as_of_day}' AS TIMESTAMP(0) WITH TIME ZONE) AS as_of_day
            FROM {self.source_schema}.{self.source_table}
            WHERE value_day = DATE '{value_day}'
        """)

        if self.gather_stats:
            print(f'Start gathering stats for {self.target_schema}.{self.target_table}')
            delta_load_helper.gather_table_stats()
            print('End gathering stats')