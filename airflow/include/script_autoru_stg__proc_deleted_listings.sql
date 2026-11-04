drop table if exists iceberg.autoru_stg.proc_deleted_listings;
create table iceberg.autoru_stg.proc_deleted_listings as (
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
            cj.valid_to,
            cj.active_flag,
            pl.value_day,
            pl.as_of_day,
            pl.job_insert,
            pl.job_update
    from iceberg.autoru_stg.proc_active_listings pl
    left join iceberg.autoru_stg.stg_autoru_listings sl 
      on pl.auto_ru_id = sl.auto_ru_id
    cross join (
        select sl.value_day as valid_to, False as active_flag
        from iceberg.autoru_stg.stg_autoru_listings sl
        limit 1
    ) cj
    where sl.auto_ru_id is null
);