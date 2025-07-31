# Creating a List
List1 = []
print(len(List1))

# Creating a List of numbers
List2 = [10, 20, 14]
print(len(List2))

# Python program to demonstrate
# Addition of elements in a List

# Creating a List
List = []
print("Initial blank List: ")
print(List)

# Addition of Elements
# in the List
List.append(1)
List.append(2)
List.append(4)
print("\nList after Addition of Three elements: ")
print(List)

# Adding elements to the List
# using Iterator
for i in range(1, 4):
    List.append(i)
print("\nList after Addition of elements from 1-3: ")
print(List)

# Adding Tuples to the List
List.append((5, 6))
print("\nList after Addition of a Tuple: ")
print(List)

# Addition of List to a List
List2 = ['For', 'Geeks']
List.append(List2)
print("\nList after Addition of a List: ")
print(List)

# Python program to demonstrate 
# Addition of elements in a List
 
# Creating a List
List = [1,2,3,4]
print("Initial List: ")
print(List)

# Addition of Element at 
# specific Position
# (using Insert Method)
List.insert(3, 12)
List.insert(0, 'Geeks')
print("\nList after performing Insert Operation: ")
print(List)

# Python program to demonstrate
# Addition of elements in a List

# Creating a List
List = [1, 2, 3, 4]
print("Initial List: ")
print(List)

# Addition of multiple elements
# to the List at the end
# (using Extend Method)
List.extend([8, 'Geeks', 'Always'])
print("\nList after performing Extend Operation: ")
print(List)

# Reversing a list
mylist = [1, 2, 3, 4, 5, 'Geek', 'Python']
mylist.reverse()
print(mylist)

# Python program to demonstrate
# Removal of elements in a List

# Creating a List
List = [1, 2, 3, 4, 5, 6,
        7, 8, 9, 10, 11, 12]
print("Initial List: ")
print(List)

# Removing elements from List
# using Remove() method
List.remove(5)
List.remove(6)
print("\nList after Removal of two elements: ")
print(List)

List = [1, 2, 3, 4, 5]

# Removing element from the
# Set using the pop() method
List.pop()
print("\nList after popping an element: ")
print(List)

# Removing element at a
# specific location from the
# Set using the pop() method
List.pop(2)
print("\nList after popping a specific element: ")
print(List)


#List Comprehension
#Synatx:- newList = [ expression(element) for element in oldList if condition ]
odd_square = [x ** 2 for x in range(1, 11) if x % 2 == 1]
print(odd_square)

# Python code to demonstrate the working of
# len(), min() and max()
# initializing list 1
lis = [2, 1, 3, 5, 4]

# using len() to print length of list
print ("The length of list is : ", end="")
print (len(lis))

# using min() to print minimum element of list
print ("The minimum element of list is : ", end="")
print (min(lis))

# using max() to print maximum element of list
print ("The maximum element of list is : ", end="")
print (max(lis))

# Python code to demonstrate the working of
# index() and count()
# initializing list 1
lis = [2, 1, 3, 5, 4, 3]

# using index() to print first occurrence of 3
# prints 5
print ("The first occurrence of 3 after 3rd position is : ", end="")
print (lis.index(3, 3, 6))

# using count() to count number of occurrence of 3
print ("The number of occurrences of 3 is : ", end="")
print (lis.count(3))