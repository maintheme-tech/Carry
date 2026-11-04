drop table if exists iceberg.autoru_stg.proc_updated_listings;
create table iceberg.autoru_stg.proc_updated_listings as (
    select  pl.auto_ru_id,
            sl.url,
            sl.model_title,
            sl.year,
            sl.mileage,
            sl.price,
            sl.engine_volume,
            sl.power_hp,
            sl.power_kw,
            sl.fuel,
            sl.body_type,
            sl.drive,
            sl.transmission,
            sl.sale_status,
            sl.color,
            sl.complectation,
            sl.seller,
            sl.seller_profile_url,
            sl.seller_verified,
            sl.seller_rating,
            sl.seller_region,
            sl.seller_address,
            sl.photo_count,
            sl.photo_urls,
            sl.badges,
            sl.value_day as valid_from,
            date '5999-12-01' as valid_to,
            True as active_flag,
            sl.value_day,
            pl.as_of_day,
            pl.job_insert,
            sl.job_update
    from iceberg.autoru_stg.stg_autoru_listings sl
    join iceberg.autoru_stg.proc_active_listings pl
      on sl.auto_ru_id = pl.auto_ru_id
    where sl.hashed_columns != pl.hashed_values
);

drop table if exists iceberg.autoru_stg.proc_closed_listings;
create table iceberg.autoru_stg.proc_closed_listings as (
    select  pl.auto_ru_id,
            pl.url,
            pl.model_title,
            pl.year,
            pl.mileage,
            pl.price,
            pl.engine_volume,
            pl.power_hp,
            pl.power_kw,
            pl.fuel,
            pl.body_type,
            pl.drive,
            pl.transmission,
            pl.sale_status,
            pl.color,
            pl.complectation,
            pl.seller,
            pl.seller_profile_url,
            pl.seller_verified,
            pl.seller_rating,
            pl.seller_region,
            pl.seller_address,
            pl.photo_count,
            pl.photo_urls,
            pl.badges,
            pl.valid_from,
            sl.value_day as valid_to,
            False as active_flag,
            sl.value_day,
            pl.as_of_day,
            pl.job_insert,
            sl.job_update
    from iceberg.autoru_stg.stg_autoru_listings sl
    join iceberg.autoru_stg.proc_active_listings pl
      on sl.auto_ru_id = pl.auto_ru_id
    where sl.hashed_columns != pl.hashed_values
);