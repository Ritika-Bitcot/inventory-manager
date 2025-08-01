# Creating an empty Tuple
Tuple1 = ()
print("Initial empty Tuple: ")
print(Tuple1)

# Creating a Tuple
# with the use of string
Tuple1 = ("Geeks", "For")
print("\nTuple with the use of String: ")
print(Tuple1)

# Creating a Tuple with
# the use of list
list1 = [1, 2, 4, 5, 6]
print("\nTuple using List: ")
print(tuple(list1))

# Creating a Tuple
# with the use of built-in function
Tuple1 = tuple("Geeks")
print("\nTuple with the use of function: ")
print(Tuple1)

# Creating a Tuple
# with Mixed Datatype
Tuple1 = (5, "Welcome", 7, "Geeks")
print("\nTuple with Mixed Datatypes: ")
print(Tuple1)

# Creating a Tuple
# with nested tuples
Tuple1 = (0, 1, 2, 3)
Tuple2 = ("python", "geek")
Tuple3 = (Tuple1, Tuple2)
print("\nTuple with nested tuples: ")
print(Tuple3)

# Creating a Tuple
# with repetition
Tuple1 = ("Geeks",) * 3
print("\nTuple with repetition: ")
print(Tuple1)

# Creating a Tuple
# with the use of loop
Tuple1 = "Geeks"
n = 5
print("\nTuple with a loop")
for i in range(int(n)):
    Tuple1 = (Tuple1,)
    print(Tuple1)

# Concatenation of tuples
Tuple1 = (0, 1, 2, 3)
Tuple2 = ("Geeks", "For", "Geeks")

Tuple3 = Tuple1 + Tuple2

print("\nTuples after Concatenation: ")
print(Tuple3)

# Deleting a Tuple

Tuple1 = (0, 1, 2, 3, 4)
del Tuple1
# Slicing of a Tuple

# Slicing of a Tuple
# with Numbers
Tuple1 = tuple("GEEKSFORGEEKS")

# Removing First element
print("Removal of First Element: ")
print(Tuple1[1:])

# Reversing the Tuple
print("\nTuple after sequence of Element is reversed: ")
print(Tuple1[::-1])

# Printing elements of a Range
print("\nPrinting elements between Range 4-9: ")
print(Tuple1[4:9])
