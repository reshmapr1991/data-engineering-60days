from kafka import KafkaConsumer
import json

# connect to Kafka and subscribe to "orders" topic
consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",    # read from beginning
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Consumer started — waiting for messages...")
print("="*40)

total_revenue = 0
order_count   = 0

for message in consumer:
    order = message.value

    # process the order
    total_revenue += order["amount"]
    order_count   += 1

    print(f"Received: {order['order_id']} | "
          f"{order['customer']} | "
          f"{order['product']} | "
          f"₹{order['amount']:,}")
    print(f"Running total: {order_count} orders | "
          f"Revenue: ₹{total_revenue:,}")
    print("-"*40)