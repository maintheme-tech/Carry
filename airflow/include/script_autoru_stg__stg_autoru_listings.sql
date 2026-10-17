TRUNCATE TABLE {self.target_schema}.{self.target_table}
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
            WHERE value_day = DATE '{value_day}';