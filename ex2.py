pipeline_name = "sales_etl"
records_processed = 142500
success = True
duration_seconds = 47.3
tags = ["daily", "crm", "production"]
config = {"source": "postgres", "destination": "s3"}

status = "SUCCESS" if success else "FAILED"
print(f"Pipeline: {pipeline_name} | Records: {records_processed:,} | Status: {status} | Duration: {duration_seconds}s")
print(f"Tags: {', '.join(tags)}")
print(f"Source: {config['source']} → Destination: {config['destination']}")

# Bonus
for name, val in [("pipeline_name", pipeline_name), ("records_processed", records_processed),
                   ("success", success), ("duration_seconds", duration_seconds)]:
    print(f"{name}: {type(val).__name__}")