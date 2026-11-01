DROP TABLE IF EXISTS iceberg.autoru_stg.proc_active_listings;

CREATE TABLE iceberg.autoru_stg.proc_active_listings AS (
    select *
    from iceberg.autoru_core.listings_history lh
    where lh.valid_to = DATE '5999-01-01'
);