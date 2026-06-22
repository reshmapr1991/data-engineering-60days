events_per_second = 3500
bytes_per_event = 512
retention_days = 90
cost_per_gb_month = 0.023

events_per_day = events_per_second * 60 * 60 * 24
total_events = events_per_day * retention_days
total_bytes = total_events * bytes_per_event
total_gb = total_bytes / (1024 ** 3)
monthly_cost = (total_gb / retention_days * 30) * cost_per_gb_month
processing_pct = (4 / 24) * 100

print(f"Events/day: {events_per_day:,}")
print(f"Total events ({retention_days}d): {total_events:,}")
print(f"Raw size: {total_gb:,.1f} GB")
print(f"Monthly cost: ${monthly_cost:,.2f}")
print(f"Processing window: {processing_pct:.2f}% of day")