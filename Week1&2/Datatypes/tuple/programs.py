# Python code to sort a list of tuples
# according to given key.


# get the last key.
def last(n):
    return n[m]


# function to sort the tuple
def sort(tuples):

    # We pass used defined function last
    # as a parameter.
    return sorted(tuples, key=last)


a = [(23, 45, 20), (25, 44, 39), (89, 40, 23)]
m = 2
print("Sorted:"),
print(sort(a))


# Python program to remove empty tuples from a
# list of tuples function to remove empty tuples
# using list comprehension
def Remove(tuples):
    tuples = [t for t in tuples if t]
    return tuples


tuples = [
    (),
    ("ram", "15", "8"),
    (),
    ("laxman", "sita"),
    ("krishna", "akbar", "45"),
    ("", ""),
    (),
]
print(Remove(tuples))
