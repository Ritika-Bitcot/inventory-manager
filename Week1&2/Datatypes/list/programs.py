from collections import Counter


# Python code to sort a list by creating
def Sorting(lst):
    lst2 = sorted(lst, key=len)
    return lst2


lst = ["rohan", "amy", "sapna", "muhammad", "aakash", "raunak", "chinmoy"]
print(Sorting(lst))

# Program to print duplicates from a list of integers

l1 = [1, 2, 1, 2, 3, 4, 5, 1, 1, 2, 5, 6, 7, 8, 9, 9]
d = Counter(l1)
print(d)

new_list = list([item for item in d if d[item] > 1])
print(new_list)

# Check if a List is Palindrome
nums = [1, 2, 3, 2, 1]
if nums == nums[::-1]:
    print("Palindrome")
else:
    print("Not Palindrome")

# Find Second Largest Number in a List
nums = [12, 8, 5, 6, 3, 2, 4, 1]
f = s = float("-inf")
for i in range(len(nums)):
    if nums[i] > f:
        s = f
        f = nums[i]
    elif nums[i] > s and nums[i] != f:
        s = nums[i]
print(s)

# Remove Duplicates from a List
numbers = [1, 2, 2, 3, 4, 4, 5]
unique = list(set(numbers))
print("Unique list:", unique)

nums = [2, 4, 3, 5, 7, 8]
target = 10
hash = {}
for i in range(len(nums)):
    j = target - nums[i]
    if j in hash.keys():
        print(f"Pair: ({nums[i]}, {nums[j]})")
    else:
        hash[i] = i

# Rotate List to the Right by K Positions
nums = [1, 2, 3, 4, 5]
k = 2
k = k % len(nums)  # handle k > len
rotated = nums[-k:] + nums[:-k]
print("Rotated List:", rotated)
