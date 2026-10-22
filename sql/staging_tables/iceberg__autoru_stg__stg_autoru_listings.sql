DROP TABLE iceberg.autoru_stg.stg_autoru_listings;
CREATE OR REPLACE TABLE iceberg.autoru_stg.stg_autoru_listings (
    auto_ru_id          BIGINT,
    url                 VARCHAR,
    model_title         VARCHAR, -- need to split later
    year                INT,
    mileage             BIGINT,
    price               BIGINT,
    engine_volume       DOUBLE, 
    power_hp            VARCHAR,        
    power_kw            VARCHAR,
    fuel                VARCHAR,
    body_type           VARCHAR,
    drive               VARCHAR,
    transmission        VARCHAR,
    sale_status         VARCHAR,
    color               VARCHAR,
    complectation       VARCHAR,
    seller              VARCHAR,
    seller_profile_url  VARCHAR,
    seller_verified     BOOLEAN,
    seller_rating       VARCHAR,
    seller_region       VARCHAR,
    seller_address      VARCHAR,
    photo_count         INT,
    photo_urls          ARRAY(VARCHAR),
    badges              ARRAY(VARCHAR),
    value_day           DATE,
    as_of_day           TIMESTAMP(0) WITH TIME ZONE,
    job_insert          BIGINT,
    job_update          BIGINT
)
WITH (
    format = 'PARQUET'
);