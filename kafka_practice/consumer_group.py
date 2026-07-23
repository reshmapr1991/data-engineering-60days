from kafka import KafkaConsumer
import json
import sys

# get consumer name from command line
consumer_name = sys.argv[1] if len(sys.argv) > 1 else "consumer1"

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9092",
    group_id="order_processors",    # same group_id = share messages
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print(f"{consumer_name} started — waiting for messages...")
print("="*40)

for message in consumer:
    order = message.value
    print(f"{consumer_name} processing: "
          f"{order['order_id']} | "
          f"{order['customer']} | "
          f"₹{order['amount']:,}")