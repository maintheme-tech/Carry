drop table iceberg.autoru_core.actual_listings;
CREATE OR REPLACE TABLE iceberg.autoru_core.actual_listings (
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
    format = 'PARQUET',
    partitioning = array['value_day']
);

DELETE FROM iceberg.tables_metadata.md_columns
WHERE schema_name = 'iceberg.autoru_core'
  AND table_name  = 'actual_listings';

INSERT INTO iceberg.tables_metadata.md_columns (
    schema_name,
    table_name,
    column_name,
    ordinal_position,
    data_type,
    primary_key_flag,
    on_match_update_flag,
    partitioned_by_flag,
    active_flag,
    description
)
VALUES
    ('iceberg.autoru_core', 'actual_listings', 'auto_ru_id',          1,  'BIGINT',                      TRUE,  FALSE, FALSE, TRUE, 'Уникальный ID объявления Auto.ru'),
    ('iceberg.autoru_core', 'actual_listings', 'url',                 2,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'URL объявления'),
    ('iceberg.autoru_core', 'actual_listings', 'model_title',         3,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Название модели'),
    ('iceberg.autoru_core', 'actual_listings', 'year',                4,  'INTEGER',                     FALSE, TRUE,  FALSE, TRUE, 'Год выпуска'),
    ('iceberg.autoru_core', 'actual_listings', 'mileage',             5,  'BIGINT',                      FALSE, TRUE,  FALSE, TRUE, 'Пробег автомобиля'),
    ('iceberg.autoru_core', 'actual_listings', 'price',               6,  'BIGINT',                      FALSE, TRUE,  FALSE, TRUE, 'Цена автомобиля'),
    ('iceberg.autoru_core', 'actual_listings', 'engine_volume',       7,  'DOUBLE',                      FALSE, TRUE,  FALSE, TRUE, 'Объём двигателя'),
    ('iceberg.autoru_core', 'actual_listings', 'power_hp',            8,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Мощность двигателя в л.с.'),
    ('iceberg.autoru_core', 'actual_listings', 'power_kw',            9,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Мощность двигателя в кВт'),
    ('iceberg.autoru_core', 'actual_listings', 'fuel',               10,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Тип топлива'),
    ('iceberg.autoru_core', 'actual_listings', 'body_type',          11,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Тип кузова'),
    ('iceberg.autoru_core', 'actual_listings', 'drive',              12,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Тип привода'),
    ('iceberg.autoru_core', 'actual_listings', 'transmission',       13,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Тип коробки передач'),
    ('iceberg.autoru_core', 'actual_listings', 'sale_status',        14,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Статус продажи'),
    ('iceberg.autoru_core', 'actual_listings', 'color',              15,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Цвет автомобиля'),
    ('iceberg.autoru_core', 'actual_listings', 'complectation',      16,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Комплектация'),
    ('iceberg.autoru_core', 'actual_listings', 'seller',             17,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Продавец'),
    ('iceberg.autoru_core', 'actual_listings', 'seller_profile_url', 18,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'URL профиля продавца'),
    ('iceberg.autoru_core', 'actual_listings', 'seller_verified',    19,  'BOOLEAN',                     FALSE, TRUE,  FALSE, TRUE, 'Признак верификации продавца'),
    ('iceberg.autoru_core', 'actual_listings', 'seller_rating',      20,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Рейтинг продавца'),
    ('iceberg.autoru_core', 'actual_listings', 'seller_region',      21,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Регион продавца'),
    ('iceberg.autoru_core', 'actual_listings', 'seller_address',     22,  'VARCHAR',                     FALSE, TRUE,  FALSE, TRUE, 'Адрес продавца'),
    ('iceberg.autoru_core', 'actual_listings', 'photo_count',        23,  'INTEGER',                     FALSE, TRUE,  FALSE, TRUE, 'Количество фотографий'),
    ('iceberg.autoru_core', 'actual_listings', 'photo_urls',         24,  'ARRAY(VARCHAR)',              FALSE, TRUE,  FALSE, TRUE, 'Список URL фотографий'),
    ('iceberg.autoru_core', 'actual_listings', 'badges',             25,  'ARRAY(VARCHAR)',              FALSE, TRUE,  FALSE, TRUE, 'Список бейджей объявления'),
    ('iceberg.autoru_core', 'actual_listings', 'value_day',          26,  'DATE',                        FALSE, FALSE, TRUE,  TRUE, 'Дата актуальности записи'),
    ('iceberg.autoru_core', 'actual_listings', 'as_of_day',          27,  'TIMESTAMP(0) WITH TIME ZONE', FALSE, FALSE,  FALSE, TRUE, 'Дата и время вставки записи в хранилище'),
    ('iceberg.autoru_core', 'actual_listings', 'job_insert',         28,  'BIGINT',                     FALSE, FALSE, FALSE, TRUE, 'Run ID DAG, впервые вставившего запись'),
    ('iceberg.autoru_core', 'actual_listings', 'job_update',         29,  'BIGINT',                     FALSE, TRUE,  FALSE, TRUE, 'Run ID DAG, последним обновившего запись');