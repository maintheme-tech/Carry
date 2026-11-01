DROP TABLE IF EXISTS iceberg.autoru_stg.proc_new_listings;

CREATE TABLE iceberg.autoru_stg.proc_new_listings AS (
    select * 
    from iceberg.autoru_stg.stg_autoru_listings sl
    left join iceberg.autoru_stg.proc_active_listings al 
    on sl.auto_ru_id = al.auto_ru_id
    where sl.auto_ru_id is null
);