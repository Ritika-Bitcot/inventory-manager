# For loop: Print even numbers from 1 to 10
print("Even numbers from 1 to 10:")
for num in range(1, 11):
    if num % 2 == 0:
        print(num)

# While loop: Countdown from 5 to 1
print("\nReverse Number:")
count = 5
while count > 0:
    print(count)
    count -= 1

# Nested loop: Print a 3x3 multiplication table
print("\nMultiplication Table:")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i * j}")

# Break and Continue statements
print("\nBreak and Continue:")
for i in range(1, 6):
    if i == 3:
        break
    print(i)

for i in range(1, 6):
    if i == 3:
        continue
    print(i)

# Pass statement
print("\nPass Statement:")
for i in range(1, 6):
    pass

# Nested loop with break
print("\nNested loop with break:")
for i in range(1, 4):
    for j in range(1, 4):
        if i == 2 and j == 2:
            break
        print(f"{i} x {j} = {i * j}")

# Nested loop with continue
print("\nNested loop with continue:")
for i in range(1, 4):
    for j in range(1, 4):
        if i == 2 and j == 2:
            continue
        print(f"{i} x {j} = {i * j}")

# Nested loop with pass
print("\nNested loop with pass:")
for i in range(1, 4):
    for j in range(1, 4):
        if i == 2 and j == 2:
            pass
        print(f"{i} x {j} = {i * j}")

#for each with skip
for each in range(1,10,2): 
    print(each,end=" ")
print()


