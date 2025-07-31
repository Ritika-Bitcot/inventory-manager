# Program to illustrate the difference between == and is

# Two variables with the same value but different objects
a = [1, 2, 3]
b = [1, 2, 3]
c = a
c[0]=12
print(a)
print("a_id:",id(a[0]),id(a[1]),id(a[2]),id(a))
print("b_id:",id(b[0]),id(b[1]),id(b[2]),id(b))
print("c_id:",id(c))
print("a == b :", a == b)  # True, because their contents (values) are equal
print("a is b :", a is b)  # False, because they are different objects in memory
print("a is c :", a is c)

# Assigning one variable to another
c = a

print("a == c :", a == c)  # True, values are equal
print("a is c :", a is c)  # True, both point to the same object

# Immutable types (like integers and strings)
x = 1000
y = 1000
print("x_id:",id(x))
print("y_id:",id(y))


print("x == y :", x == y)  # True, values are equal
print("x is y :", x is y)  # True refer to same objects in memory

# Small integers are cached in CPython
m = 10
n = 10

print("m == n :", m == n)  # True
print("m is n :", m is n)  # True (because of integer caching in CPython)

# String literals
s1 = "hello"
s2 = "hello"

print("s1_id:",id(s1))
print("s2_id:",id(s2))

print("s1 == s2 :", s1 == s2)  # True
print("s1 is s2 :", s1 is s2)  # True (strings are interned in CPython)

# Custom object identity
class MyClass:
    pass

obj1 = MyClass()
obj2 = MyClass()

print("obj1 == obj2 :", obj1 == obj2)  # False, no __eq__ method defined
print("obj1 is obj2 :", obj1 is obj2)  # False, different instances

obj3 = obj1
print("obj1 is obj3 :", obj1 is obj3)  # True, same object

