import io
import json

import pyarrow as pa
import pyarrow.parquet as pq

# ---------------------------------------------------------------------------
# Схема Parquet (зафиксирована, чтобы Trino видел стабильные типы)
# ---------------------------------------------------------------------------

SCHEMA = pa.schema([
    ("auto_ru_id", pa.string()),
    ("url", pa.string()),
    ("model_title", pa.string()),
    ("year", pa.int32()),
    ("mileage", pa.int64()),
    ("price", pa.int64()),
    ("engine_volume", pa.string()),
    ("power", pa.string()),
    ("fuel", pa.string()),
    ("body_type", pa.string()),
    ("drive", pa.string()),
    ("transmission", pa.string()),
    ("sale_status", pa.string()),
    ("color", pa.string()),
    ("complectation", pa.string()),
    ("seller", pa.string()),
    ("seller_profile_url", pa.string()),
    ("seller_verified", pa.bool_()),
    ("seller_rating", pa.string()),
    ("seller_region", pa.string()),
    ("seller_address", pa.string()),
    ("photo_count", pa.int32()),
    ("photo_urls", pa.list_(pa.string())),
    ("badges", pa.list_(pa.string())),
])


def ndjson_to_parquet(s3, bucket, source_prefix, target_key):

    keys = s3.list_keys(bucket_name=bucket, prefix=source_prefix)

    print('Started conversion')

    records = []
    for key in keys:
        obj = s3.get_key(key=key, bucket_name=bucket)
        raw = obj.get()["Body"].read().decode("utf-8")
        for line in raw.splitlines():
            line = line.strip()
            if line:
                records.append(json.loads(line))
    
    print('Conversion finished')

    print('Started parquet generation')
    table = pa.Table.from_pylist(records, schema=SCHEMA)

    buf = io.BytesIO()
    pq.write_table(table, buf, compression="snappy")
    buf.seek(0)

    s3.load_bytes(
        bytes_data=buf.getvalue(),
        key=target_key,
        bucket_name=bucket,
        replace=True,
    )

    print(f'{bucket}/{target_key} successfully loaded')