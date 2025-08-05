"""
Violation of SRP:

def process_scores(scores)->None:
    total = sum(scores)
    average = total / len(scores)
    print(f"Total: {total}, Average: {average}")

Problem: Calculates and prints scores. It is not SRP-friendly.

"""


def calculate_total(scores: list) -> float:
    """
    Calculate the total of the given scores.
    """
    return sum(scores)


def calculate_average(scores: list) -> float:
    """
    Calculate the average of the given scores.
    """
    return sum(scores) / len(scores)


def print_scores(total: float, average: float) -> None:
    """
    Print the total and average of the given scores.
    """
    print(f"Total: {total}, Average: {average}")


marks = [80, 90, 75]
total = calculate_total(marks)
avg = calculate_average(marks)
print_scores(total, avg)
