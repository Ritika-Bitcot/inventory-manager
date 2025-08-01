"""
Violation of SRP:

def get_input_and_check_even()->None:
    number = int(input("Enter a number: "))
    if number % 2 == 0:
        print("Even")
    else:
        print("Odd")

Problem: Input + logic + output = Too many responsibilities.

"""


def get_user_input() -> int:
    """
    Get user input and return the integer.
    """
    return int(input("Enter a number: "))


def is_even(num: int) -> bool:
    """
    Determine if a given integer is even.
    """
    return num % 2 == 0


def print_even_status(is_even_flag: bool) -> None:
    """
    Print "Even" if the given flag is True, otherwise print "Odd".
    """
    print("Even" if is_even_flag else "Odd")


num = get_user_input()
even_flag = is_even(num)
print_even_status(even_flag)
