CREATE TABLE IF NOT EXISTS dm.market_daily_aggregating
(
    snapshot_date Date,
    model_title String,
    year Int32,
    seller_region String,
    fuel String,
    priced_listing_count AggregateFunction(count),
    avg_price AggregateFunction(avg, Float64),
    median_price AggregateFunction(quantileTDigest(0.5), Float64)
)
ENGINE = AggregatingMergeTree
PARTITION BY toYYYYMM(snapshot_date)
ORDER BY (snapshot_date, seller_region, model_title, year, fuel);
