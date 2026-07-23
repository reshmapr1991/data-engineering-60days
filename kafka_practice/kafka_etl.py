from kafka import KafkaProducer, KafkaConsumer
import json
import threading
import time

# ── PRODUCER FUNCTION ─────────────────────────────────────────────────────────
def run_producer():
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    sales_events = [
        {"event": "sale", "product": "Laptop",     "qty": 2, "price": 75000, "region": "North"},
        {"event": "sale", "product": "Phone",      "qty": 3, "price": 45000, "region": "South"},
        {"event": "sale", "product": "Tablet",     "qty": 1, "price": 32000, "region": "East"},
        {"event": "sale", "product": "Headphones", "qty": 5, "price": 8000,  "region": "West"},
        {"event": "sale", "product": "Laptop",     "qty": 1, "price": 75000, "region": "North"},
    ]

    print("Producer: sending sales events...")
    for event in sales_events:
        producer.send("sales_events", value=event)
        print(f"Producer sent: {event['product']} | qty:{event['qty']} | region:{event['region']}")
        time.sleep(0.5)

    producer.flush()
    producer.close()
    print("Producer: all events sent!")

# ── CONSUMER FUNCTION ─────────────────────────────────────────────────────────
def run_consumer():
    consumer = KafkaConsumer(
        "sales_events",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        consumer_timeout_ms=10000,    # stop after 10 seconds of no messages
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    print("Consumer: waiting for sales events...")

    # aggregation
    region_revenue = {}
    product_qty    = {}
    total_revenue  = 0

    for message in consumer:
        event    = message.value
        revenue  = event["qty"] * event["price"]
        region   = event["region"]
        product  = event["product"]

        # update aggregations
        total_revenue              += revenue
        region_revenue[region]      = region_revenue.get(region, 0) + revenue
        product_qty[product]        = product_qty.get(product, 0) + event["qty"]

        print(f"Consumer processed: {product} | "
              f"revenue: ₹{revenue:,} | "
              f"region: {region}")

    # final report
    print("\n" + "="*40)
    print("REAL TIME SALES REPORT")
    print("="*40)
    print(f"Total revenue: ₹{total_revenue:,}")
    print("\nRevenue by region:")
    for region, rev in sorted(region_revenue.items()):
        print(f"  {region}: ₹{rev:,}")
    print("\nQuantity by product:")
    for product, qty in sorted(product_qty.items()):
        print(f"  {product}: {qty} units")
    print("="*40)

# ── RUN BOTH TOGETHER ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    # start consumer in background thread
    consumer_thread = threading.Thread(target=run_consumer)
    consumer_thread.start()

    # wait a moment then start producer
    time.sleep(2)
    run_producer()

    # wait for consumer to finish
    consumer_thread.join()
    print("ETL pipeline complete!")