from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
import json
import time

# ── CREATE TOPICS ─────────────────────────────────────────────────────────────
admin = KafkaAdminClient(bootstrap_servers="localhost:9092")

topics = [
    NewTopic(name="orders",        num_partitions=3, replication_factor=1),
    NewTopic(name="payments",      num_partitions=2, replication_factor=1),
    NewTopic(name="notifications", num_partitions=1, replication_factor=1),
]

try:
    admin.create_topics(new_topics=topics)
    print("Topics created!")
except Exception as e:
    print(f"Topics may already exist: {e}")

# ── PRODUCER — send to different topics ───────────────────────────────────────
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# send to orders topic
producer.send("orders", value={"order_id": "O011", "amount": 50000})
print("Sent to orders topic")

# send to payments topic
producer.send("payments", value={"payment_id": "P001", "status": "success"})
print("Sent to payments topic")

# send to notifications topic
producer.send("notifications", value={"user": "Rahul", "message": "Order confirmed!"})
print("Sent to notifications topic")

producer.flush()
producer.close()
print("Done!")