# Each row from a CRM export looks like:
row1 = {"customer_id": "C001", "age": 29,  "email": "alice@acme.com", "revenue": 4200.0}
row2 = {"customer_id": "",     "age": -5,  "email": "not-an-email",   "revenue": None}
row3 = {"customer_id": "C003", "age": 150, "email": "bob@co.com",     "revenue": 0.0}

# Write: def check_row(row) -> dict
# It should return a dict with:
# {
#   "valid": True/False,
#   "errors": ["list of error messages"]
# }

# Rules:
# - customer_id must not be empty
# - age must be between 1 and 120
# - email must contain "@" and "."
# - revenue must not be None and must be >= 0

# row1 → valid: True,  errors: []
# row2 → valid: False, errors: [4 messages]
# row3 → valid: False, errors: ["age out of range: 150"]

def check_row(row):
    errors =[]
    dict ={
           "valid": True/False,
           "errors": ["list of error messages"]
          }

