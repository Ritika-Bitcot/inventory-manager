# Check if Element Exists in a Set

s = {10, 20, 30}
print(20 in s)

# Find Union of Two Sets
a = {1, 2, 3}
b = {3, 4, 5}
print(a | b)

# Find Intersection of Two Sets
a = {1, 2, 3}
b = {2, 3, 4}
print(a & b)

# Find Elements in One Set but Not in Another (Difference)

a = {1, 2, 3}
b = {2, 3, 4}
print(a - b)

# Check if Two Sets are Disjoint
a = {1, 2}
b = {3, 4}
print(a.isdisjoint(b))

# Find Symmetric Difference Between Two Sets
a = {1, 2, 3}
b = {3, 4, 5}
print(a ^ b)  # {1, 2, 4, 5}

# Remove Duplicates from a List Using Set
lst = [1, 2, 2, 3, 4, 4]
unique = list(set(lst))
print(unique)

# Check if One Set is Subset or Superset of Another
a = {1, 2}
b = {1, 2, 3, 4}
print(a.issubset(b))
print(b.issuperset(a))
