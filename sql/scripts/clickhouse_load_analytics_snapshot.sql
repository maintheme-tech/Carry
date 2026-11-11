-- Pass snapshot_date, iceberg_url, s3_access_key_id, and s3_secret_access_key
-- as ClickHouse query parameters. For example, snapshot_date is the date the
-- upstream Iceberg table was refreshed.

-- Reprocessing a date removes its previous snapshot and derived aggregates.
-- The Airflow loader runs each statement with mutations_sync=2.

ALTER TABLE dm.autoru_listings_snapshot
    DELETE WHERE snapshot_date = {snapshot_date:Date};

ALTER TABLE dm.autoru_listings_current
    DELETE WHERE snapshot_date = {snapshot_date:Date};

ALTER TABLE dm.market_daily_summing
    DELETE WHERE snapshot_date = {snapshot_date:Date};

ALTER TABLE dm.market_daily_aggregating
    DELETE WHERE snapshot_date = {snapshot_date:Date};

INSERT INTO dm.autoru_listings_snapshot
(
    snapshot_date,
    auto_ru_id,
    url,
    model_title,
    year,
    mileage,
    price,
    fuel,
    seller_region,
    sale_status,
    job_update
)
SELECT
    {snapshot_date:Date},
    toUInt64(auto_ru_id),
    ifNull(url, ''),
    ifNull(model_title, ''),
    toInt32(ifNull(year, 0)),
    toUInt64(ifNull(mileage, 0)),
    toUInt64(ifNull(price, 0)),
    ifNull(fuel, ''),
    ifNull(seller_region, ''),
    ifNull(sale_status, ''),
    toUInt64(ifNull(job_update, 0))
FROM icebergS3(
    {iceberg_url:String},
    {s3_access_key_id:String},
    {s3_secret_access_key:String}
);

-- ReplacingMergeTree keeps the latest imported version for each listing.
INSERT INTO dm.autoru_listings_current
(
    auto_ru_id,
    url,
    model_title,
    year,
    mileage,
    price,
    fuel,
    seller_region,
    sale_status,
    snapshot_date,
    snapshot_version,
    job_update
)
SELECT
    auto_ru_id,
    url,
    model_title,
    year,
    mileage,
    price,
    fuel,
    seller_region,
    sale_status,
    snapshot_date,
    toYYYYMMDD(snapshot_date),
    job_update
FROM dm.autoru_listings_snapshot
WHERE snapshot_date = {snapshot_date:Date};

INSERT INTO dm.market_daily_summing
(
    snapshot_date,
    model_title,
    year,
    seller_region,
    fuel,
    listing_count,
    priced_listing_count,
    price_sum,
    mileage_listing_count,
    mileage_sum
)
SELECT
    snapshot_date,
    model_title,
    year,
    seller_region,
    fuel,
    count(),
    countIf(price > 0),
    sumIf(price, price > 0),
    countIf(mileage > 0),
    sumIf(mileage, mileage > 0)
FROM dm.autoru_listings_snapshot
WHERE snapshot_date = {snapshot_date:Date}
GROUP BY snapshot_date, model_title, year, seller_region, fuel;

-- This table contains price-bearing listings only; its aggregate states can
-- be merged again when querying across parts or dates.
INSERT INTO dm.market_daily_aggregating
(
    snapshot_date,
    model_title,
    year,
    seller_region,
    fuel,
    priced_listing_count,
    avg_price,
    median_price
)
SELECT
    snapshot_date,
    model_title,
    year,
    seller_region,
    fuel,
    countState(),
    avgState(toFloat64(price)),
    quantileTDigestState(0.5)(toFloat64(price))
FROM dm.autoru_listings_snapshot
WHERE snapshot_date = {snapshot_date:Date}
  AND price > 0
GROUP BY snapshot_date, model_title, year, seller_region, fuel;
