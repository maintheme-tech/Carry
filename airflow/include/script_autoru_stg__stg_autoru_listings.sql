TRUNCATE TABLE {self.target_schema}.{self.target_table};

INSERT INTO {self.target_schema}.{self.target_table} (
    auto_ru_id, url, model_title, year, mileage, price, engine_volume,
    power_hp, power_kw, fuel, body_type, drive, transmission, sale_status,
    color, complectation, seller, seller_profile_url, seller_verified,
    seller_rating, seller_region, seller_address, photo_count, photo_urls,
    badges, value_day, as_of_day, job_insert, job_update, hashdiff_key
)
WITH src AS (
    SELECT
        TRY_CAST(auto_ru_id AS BIGINT) AS auto_ru_id,
        url,
        model_title,
        CAST(year AS INTEGER) AS year,
        mileage,
        price,
        CASE
            WHEN engine_volume IS NULL OR TRIM(engine_volume) = '' THEN NULL
            WHEN REGEXP_LIKE(LOWER(engine_volume), '(л\.?с|hp|квт|kw)') THEN NULL
            ELSE TRY_CAST(
                    REPLACE(
                        REGEXP_EXTRACT(engine_volume, '([0-9]+([.,][0-9]+)?)'),
                        ',', '.'
                    ) AS DOUBLE
                )
        END AS engine_volume,
        CASE
            WHEN power IS NOT NULL AND TRIM(power) <> ''
                AND REGEXP_LIKE(LOWER(power), '(л\.?с|hp)')
                THEN TRIM(power)
            WHEN engine_volume IS NOT NULL AND TRIM(engine_volume) <> ''
                AND REGEXP_LIKE(LOWER(engine_volume), '(л\.?с|hp)')
                THEN TRIM(engine_volume)
            ELSE NULL
        END AS power_hp,
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
        CAST(photo_count AS INTEGER) AS photo_count,
        photo_urls,
        badges,
        value_day
    FROM (
        SELECT DISTINCT *
        FROM {self.source_schema}.{self.source_table}
        WHERE value_day = DATE '{self.value_day}'
    ) raw
)
SELECT
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
    CAST('{self.as_of_day}' AS TIMESTAMP(0) WITH TIME ZONE) AS as_of_day,
    {self.job_id} AS job_insert,
    {self.job_id} AS job_update,
    LOWER(
        TO_HEX(
            MD5(
                TO_UTF8(
                    CONCAT_WS('|',
                        CAST(auto_ru_id             AS VARCHAR),
                        COALESCE(url,                             '<null>'),
                        COALESCE(model_title,                     '<null>'),
                        CAST(COALESCE(year,           -1)         AS VARCHAR),
                        CAST(COALESCE(mileage,        -1)         AS VARCHAR),
                        CAST(COALESCE(price,          -1)         AS VARCHAR),
                        CAST(COALESCE(engine_volume,  CAST(-1.0 AS DOUBLE)) AS VARCHAR),
                        COALESCE(power_hp,                        '<null>'),
                        COALESCE(power_kw,                        '<null>'),
                        COALESCE(fuel,                            '<null>'),
                        COALESCE(body_type,                       '<null>'),
                        COALESCE(drive,                           '<null>'),
                        COALESCE(transmission,                    '<null>'),
                        COALESCE(sale_status,                     '<null>'),
                        COALESCE(color,                           '<null>'),
                        COALESCE(complectation,                   '<null>'),
                        COALESCE(seller,                          '<null>'),
                        COALESCE(seller_profile_url,              '<null>'),
                        CAST(COALESCE(seller_verified, FALSE)     AS VARCHAR),
                        COALESCE(seller_rating,                   '<null>'),
                        COALESCE(seller_region,                   '<null>'),
                        COALESCE(seller_address,                  '<null>'),
                        CAST(COALESCE(photo_count,    -1)         AS VARCHAR),
                        COALESCE(array_join(array_sort(photo_urls), ','), '<null>'),
                        COALESCE(array_join(array_sort(badges),     ','), '<null>')
                    )
                )
            )
        )
    ) AS hashdiff_key
FROM src;