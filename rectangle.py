class Rectangle:
    def __init__(self,length,breadth):
        self.len=length
        self.bre=breadth
        self.area=length*breadth
rectangle_1=Rectangle(7,8)
print(f"The area of rectangle is:{rectangle_1.area}")