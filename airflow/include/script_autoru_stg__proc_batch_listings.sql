drop table if exists iceberg.autoru_stg.proc_batch_listings;
create table iceberg.autoru_stg.proc_batch_listings as (
    select *
    from iceberg.autoru_stg.proc_new_listings
    union all
    select * 
    from iceberg.autoru_stg.proc_deleted_listings
    union all
    select * 
    from iceberg.autoru_stg.proc_updated_listings
    union all
    select *
    from iceberg.autoru_stg.proc_closed_listings
);