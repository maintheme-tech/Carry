drop table table iceberg.tables_metadata.md_columns;
create or replace table iceberg.tables_metadata.md_columns(
    schema_name                 VARCHAR,
    table_name                  VARCHAR,
    column_name                 VARCHAR,
    ordinal_position            INTEGER,
    data_type                   VARCHAR,
    primary_key_flag            BOOLEAN,
    on_match_update_flag        BOOLEAN,
    partitioned_by_flag         BOOLEAN,
    active_flag                 BOOLEAN,
    description                 VARCHAR
)
with (
    format = 'PARQUET'
);