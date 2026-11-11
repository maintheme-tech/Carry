CREATE TABLE IF NOT EXISTS dm.market_daily_summing
(
    snapshot_date Date,
    model_title String,
    year Int32,
    seller_region String,
    fuel String,
    listing_count UInt64,
    priced_listing_count UInt64,
    price_sum UInt64,
    mileage_listing_count UInt64,
    mileage_sum UInt64
)
ENGINE = SummingMergeTree
PARTITION BY toYYYYMM(snapshot_date)
ORDER BY (snapshot_date, seller_region, model_title, year, fuel);
