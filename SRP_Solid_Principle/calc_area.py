"""
Violation of SRP:

def calculate_area_and_print(shape, value):
    if shape == "circle":
        area = 3.14 * value ** 2
    elif shape == "square":
        area = value ** 2
    print(f"The area is {area}")

Problem: This function calculates and prints. It is doing two things.

"""
def calculate_area(shape, value):
    if shape == "circle":
        return 3.14 * value ** 2
    elif shape == "square":
        return value ** 2
    else:
        return None

def print_area(area):
    print(f"The area is {area}")

area = calculate_area("circle", 5)
print_area(area)
