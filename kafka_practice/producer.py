from kafka import KafkaProducer
import json
import time

# connect to Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# simulate sending 10 orders
orders = [
    {"order_id": "O001", "customer": "Rahul",  "product": "Laptop",     "amount": 75000},
    {"order_id": "O002", "customer": "Priya",  "product": "Phone",      "amount": 45000},
    {"order_id": "O003", "customer": "Arjun",  "product": "Tablet",     "amount": 32000},
    {"order_id": "O004", "customer": "Sneha",  "product": "Headphones", "amount": 8000},
    {"order_id": "O005", "customer": "Karan",  "product": "Laptop",     "amount": 75000},
    {"order_id": "O006", "customer": "Meera",  "product": "Phone",      "amount": 45000},
    {"order_id": "O007", "customer": "Vikram", "product": "Tablet",     "amount": 32000},
    {"order_id": "O008", "customer": "Anjali", "product": "Headphones", "amount": 8000},
    {"order_id": "O009", "customer": "Rohit",  "product": "Laptop",     "amount": 75000},
    {"order_id": "O010", "customer": "Divya",  "product": "Phone",      "amount": 45000},
]

print("Starting producer...")
print("Sending orders to Kafka topic: orders")
print("="*40)

for order in orders:
    # send message to "orders" topic
    producer.send("orders", value=order)
    print(f"Sent: {order['order_id']} | {order['customer']} | {order['product']} | ₹{order['amount']:,}")
    time.sleep(1)   # wait 1 second between messages

producer.flush()   # make sure all messages are sent
print("="*40)
print("All orders sent successfully!")
producer.close()