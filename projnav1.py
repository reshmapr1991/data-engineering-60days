#The Messy Data
employees= [
    {"name": "naveen",  "age": "25", "salary": "50000",  "city": "Bengaluru"},
    {"name": "RAHUL",   "age": "abc","salary": "75000",  "city": "mumbai"},
    {"name": "Asha",    "age": "27", "salary": "-1000",  "city": "DELHI"},
    {"name": "priya",   "age": "30", "salary": "0",      "city": "Chennai"},
    {"name": "Kiran",   "age": "28", "salary": "60000",  "city": "hyderabad"},
    {"name": "VIKRAM",  "age": "35", "salary": "90000",  "city": "MUMBAI"},
    {"name": "",        "age": "22", "salary": "40000",  "city": "Bengaluru"},
    {"name": "Sneha",   "age": "29", "salary": "55000",  "city": "delhi"},
]



def cleaned_row(data):

    if data["name"] == "":
        return None

    if not data["age"].isdigit():
        return None

    data["name"] = data["name"].title()
    data["city"] = data["city"].title()
    data["age"] = int(data["age"])
    data["salary"] = int(data["salary"])
    if data["salary"] <= 0:
        return None

    return data

def run_pipe(data):
    cleaned=[]
    skipped=0
    for emp in data:
        result = cleaned_row(emp)

        if result:
            cleaned.append(result)
        else:
            skipped += 1

        return cleaned, skipped

def summary(cleaned,skipped):
    print("Total rows processed:", len(cleaned) + skipped)
    print("Total valid rows:", len(cleaned))
    print("Total skipped rows:", skipped)


    total_salary = 0

    for emp in cleaned:
        total_salary = total_salary + emp["salary"]

    avg_salary = total_salary / len(cleaned)

    print("Average salary:", avg_salary)

    print("\nValid Employees:")

    for emp in cleaned:
      print(emp)

cleaned, skipped = run_pipe(employees)
summary(cleaned, skipped)



# #         clean_list=[]
# #         x["name"] = x["name"].title()
# #         x["city"] = x["city"].title()
# #         if not x["age"].isdigit():
# #             continue
# #         x["age"]=int(x["age"])
# #         if x["name"] == "":
# #             continue
# #         x["salary"] = int(x["salary"])
# #         if x["salary"]<= 0:
# #             continue
# #
# #         print(x)
# #         clean_list.append(x)
# #
# # data_fun= cleaned_list(data)
#




