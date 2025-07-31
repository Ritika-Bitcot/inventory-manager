# Variable assignment
name = "Alice"
age = 25
height = 5.4
is_student = True

# Multiple assignments
x, y, z = 1, 2, 3

# Display types
print("---- Variable Types ----")
print(f"Type of name: {type(name)}")
print(f"Type of age: {type(age)}")
print(f"Type of height: {type(height)}")
print(f"Type of is_student: {type(is_student)}")

# Type checking
print("---- Type Checking ----")
print(isinstance(age, int))         # True
print(isinstance(height, float))    # True
print(isinstance(name, str))        # True
print(isinstance(is_student, bool)) # True
