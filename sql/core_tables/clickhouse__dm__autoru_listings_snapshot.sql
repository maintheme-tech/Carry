CREATE TABLE IF NOT EXISTS dm.autoru_listings_snapshot
(
    snapshot_date Date,
    auto_ru_id UInt64,
    url String,
    model_title String,
    year Int32,
    mileage UInt64,
    price UInt64,
    fuel String,
    seller_region String,
    sale_status String,
    job_update UInt64
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(snapshot_date)
ORDER BY (snapshot_date, seller_region, model_title, year, fuel, auto_ru_id);
