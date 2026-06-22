transactions = [
    {"region": "north", "product": "widget", "amount": 1200},
    {"region": "south", "product": "gadget", "amount": 850},
    {"region": "north", "product": "gadget", "amount": 2300},
    {"region": "east",  "product": "widget", "amount": 675},
    {"region": "south", "product": "widget", "amount": 1900},
    {"region": "north", "product": "widget", "amount": 940},
    {"region": "east",  "product": "gadget", "amount": 3100},
]

res = 0
for value in transactions.values():
    res += value
print(res)