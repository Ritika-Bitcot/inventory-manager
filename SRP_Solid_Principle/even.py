"""
Violation of SRP:

def get_input_and_check_even():
    number = int(input("Enter a number: "))
    if number % 2 == 0:
        print("Even")
    else:
        print("Odd")

Problem: Input + logic + output = Too many responsibilities.

"""

def get_user_input():
    return int(input("Enter a number: "))

def is_even(number):
    return number % 2 == 0

def print_even_status(is_even_flag):
    print("Even" if is_even_flag else "Odd")


num = get_user_input()
even_flag = is_even(num)
print_even_status(even_flag)
