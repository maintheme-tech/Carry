DROP TABLE IF EXISTS iceberg.autoru_stg.proc_active_listings;
CREATE TABLE iceberg.autoru_stg.proc_active_listings AS (
    select  lh.auto_ru_id,
            lh.url,
            lh.model_title,
            lh.year,
            lh.mileage,
            lh.price,
            lh.engine_volume,
            lh.power_hp,
            lh.power_kw,
            lh.fuel,
            lh.body_type,
            lh.drive,
            lh.transmission,
            lh.sale_status,
            lh.color,
            lh.complectation,
            lh.seller,
            lh.seller_profile_url,
            lh.seller_verified,
            lh.seller_rating,
            lh.seller_region,
            lh.seller_address,
            lh.photo_count,
            lh.photo_urls,
            lh.badges,
            lh.valid_from,
            lh.valid_to,
            lh.active_flag,
            lh.value_day,
            lh.as_of_day,
            lh.job_insert,
            lh.job_update,
            LOWER(
                TO_HEX(
                    MD5(
                        TO_UTF8(
                            CONCAT_WS('|',
                                CAST(COALESCE(CAST(auto_ru_id AS VARCHAR), '∅') AS VARCHAR),
                                COALESCE(url, '∅'),
                                COALESCE(model_title, '∅'),
                                CAST(COALESCE(year, -1) AS VARCHAR),
                                CAST(COALESCE(mileage, -1) AS VARCHAR),
                                CAST(COALESCE(price, -1) AS VARCHAR),
                                CAST(COALESCE(engine_volume, -1) AS VARCHAR),
                                COALESCE(power_hp, '∅'),
                                COALESCE(power_kw, '∅'),
                                COALESCE(fuel, '∅'),
                                COALESCE(body_type, '∅'),
                                COALESCE(drive, '∅'),
                                COALESCE(transmission, '∅'),
                                COALESCE(sale_status, '∅'),
                                COALESCE(color, '∅'),
                                COALESCE(complectation, '∅'),
                                COALESCE(seller, '∅'),
                                COALESCE(seller_profile_url, '∅'),
                                CAST(COALESCE(seller_verified, false) AS VARCHAR),
                                COALESCE(seller_rating, '∅'),
                                COALESCE(seller_region, '∅'),
                                COALESCE(seller_address, '∅'),
                                CAST(COALESCE(photo_count, -1) AS VARCHAR),
                                COALESCE(array_join(array_sort(photo_urls), ','), '∅'),
                                COALESCE(array_join(array_sort(badges), ','), '∅')
                            )
                        )
                    )
                )
            ) AS hashdiff_key
    from iceberg.autoru_core.listings_history lh
    where lh.valid_to = DATE '5999-01-01'
);