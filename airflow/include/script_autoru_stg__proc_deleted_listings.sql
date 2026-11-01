drop table if exists iceberg.autoru_stg.proc_deleted_listings;

create table iceberg.autoru_stg.proc_deleted_listings as (
    select *
    from iceberg.autoru_stg.proc_active_listings al
    left join iceberg.autoru_stg.stg_autoru_listings sl 
    on al.auto_ru_id = sl.auto_ru_id
    where al.auto_ru_id is null
)