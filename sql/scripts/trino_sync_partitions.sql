CALL hive.system.sync_partition_metadata(
    schema_name => 'autoru_raw',
    table_name  => 'raw_autoru_listings',
    mode        => 'FULL'
);