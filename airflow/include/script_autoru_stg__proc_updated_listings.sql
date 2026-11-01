drop table if exists iceberg.autoru_stg.proc_updated_listings;

create table iceberg.autoru_stg.proc_updated_listings as (
    select * 
    from iceberg.autoru_stg.stg_autoru_listings sl
    join iceberg.autoru_stg.proc_active_listings al 
    on sl.auto_ru_id = al.auto_ru_id
)