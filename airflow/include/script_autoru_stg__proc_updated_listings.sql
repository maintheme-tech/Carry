drop table if exists iceberg.autoru_stg.proc_changed_listings;
create table iceberg.autoru_stg.proc_changed_listings as (
    select * 
    from iceberg.autoru_stg.stg_autoru_listings sl
    join iceberg.autoru_stg.proc_active_listings pl
      on sl.auto_ru_id = pl.auto_ru_id
    where sl.hashed_columns != pl.hashed_values
)

drop table if exists iceberg.autoru_stg.proc_updated_listings;
create table iceberg.autoru_stg.proc_updated_listings as (
    select *
    from iceberg.autoru_stg.proc_changed_listings
)

drop table if exists iceberg.autoru_stg.proc_closed_listings;
create table iceberg.autoru_stg.proc_closed_listings as (
    select *
    from iceberg.autoru_stg.proc_changed_listings
)