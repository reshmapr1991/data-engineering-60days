def decorator_area(func):
    def wrapper_func(a,b):
        print("length is",a,"breadth is",b)
        result=func(a,b)
        return result
    return wrapper_func
@decorator_area
def area(a,b):
    return a*b

print(area(10,15))
