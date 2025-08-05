"""
Violation of SRP:

def calculate_area_and_print(shape: str, value: float)->None:
    if shape == "circle":
        area = 3.14 * value ** 2
    elif shape == "square":
        area = value ** 2
    print(f"The area is {area}")

Problem: This function calculates and prints. It is doing two things.
"""


def calculate_area(shape: str, value: float) -> float | None:
    """
    Calculate the area of a given shape.
    """

    if shape == "circle":
        return 3.14 * value**2
    elif shape == "square":
        return value**2
    else:
        return None


def print_area(area):
    """
    Print the calculated area.
    """

    print(f"The area is {area}")


area = calculate_area("circle", 5)
print_area(area)
