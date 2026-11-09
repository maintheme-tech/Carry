DROP TABLE IF EXISTS iceberg.autoru_stg.proc_new_listings;
CREATE TABLE iceberg.autoru_stg.proc_new_listings AS (
    select  sl.auto_ru_id,
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
            sl.as_of_day,
            sl.job_insert,
            sl.job_update
    from iceberg.autoru_stg.stg_autoru_listings sl
    left join iceberg.autoru_stg.proc_active_listings pl 
      on sl.auto_ru_id = pl.auto_ru_id
    where pl.auto_ru_id is null
);

analyze iceberg.autoru_stg.proc_new_listings;