cities = [
    {"city": "Bengaluru", "population": 12000000},
    {"city": "Mangalore", "population": 4500000},
    {"city": "Chennai", "population": 67000000},
    {"city": "Mysore", "population": 9500000},
    {"city": "coimbatore", "population": 3100000}
]

count = 0
for x in cities:
    if x['population'] > 5000000:
        print(f"The city  above 5 million: {x['city']}")
        count+=1

        # print the city
        # increment count

print(f"Total cities above 5 million: {count}")