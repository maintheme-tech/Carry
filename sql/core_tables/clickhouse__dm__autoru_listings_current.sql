CREATE TABLE IF NOT EXISTS dm.autoru_listings_current
(
    auto_ru_id UInt64,
    url String,
    model_title String,
    year Int32,
    mileage UInt64,
    price UInt64,
    fuel String,
    seller_region String,
    sale_status String,
    snapshot_date Date,
    snapshot_version UInt32,
    job_update UInt64
)
ENGINE = ReplacingMergeTree(snapshot_version)
ORDER BY auto_ru_id;
