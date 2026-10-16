drop table autoru_raw.raw_autoru_listings;
CREATE TABLE hive.autoru_raw.raw_autoru_listings (
    auto_ru_id          VARCHAR,
    url                 VARCHAR,
    model_title         VARCHAR,
    year                BIGINT,
    mileage             BIGINT,
    price               BIGINT,
    engine_volume       VARCHAR,
    power               VARCHAR,
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
    photo_count         BIGINT,
    photo_urls          ARRAY(VARCHAR),
    badges              ARRAY(VARCHAR),
    value_day           DATE
)
WITH (
    format = 'PARQUET',
    external_location = 's3://data/prepared_parquet/auto.ru/',
    partitioned_by = ARRAY['value_day']
);