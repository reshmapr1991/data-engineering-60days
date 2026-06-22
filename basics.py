name = "Alice"
age = 25
salary = 75000.50
is_employed = True
raw = "  hello world  "
print(raw.strip())          # remove whitespace
print(raw.strip().upper())  # HELLO WORLD
print(raw.strip().replace("world", "data engineer"))
print(f"Name: {name}, Age: {age}, Salary: {salary:.2f}")

tools = ["Python", "SQL", "Spark", "Airflow", "dbt"]
print(tools[0])        # Python
print(tools[-1])       # dbt
print(tools[1:3])      # ['SQL', 'Spark']
tools.append("Kafka")
tools.remove("dbt")
print(tools)
employee = {
    "id": 101,
    "name": "Ravi",
    "department": "Engineering",
    "salary": 90000
}
print(employee["name"])
employee["city"] = "Bengaluru"   # add new key
print(employee.keys())
print(employee.values())
for key, value in employee.items():
    print(f"{key}: {value}")
ids = [1, 2, 2, 3, 3, 3, 4]
unique_ids = set(ids)
print(unique_ids)
# For loops
sales = [1200, 3400, 900, 5600, 2100]

total = 0
for s in sales:
    total += s
print(f"Total sales: {total}")

doubled = [s * 2 for s in sales]
print(doubled)

filtered = [s for s in sales if s > 2000]
print(filtered)  # only sales above 2000

def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

avg = calculate_average(sales)
print(f"Average: {avg:.2f}")

def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

minimum, maximum, average = get_stats(sales)
print(f"Min: {minimum}, Max: {maximum}, Avg: {average:.2f}")