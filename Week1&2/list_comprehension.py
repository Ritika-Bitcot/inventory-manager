# Create a list of squares from 1 to 10
# Output: [1, 4, 9, 16, ..., 100]
sq = [x * x for x in range(11)]
print(sq)

# Get all even numbers from a list
# Input: [1,2,3,4,5,6] → Output: [2,4,6]
even = [x for x in range(10) if x % 2 == 0]
print(even)

# Convert a list of strings to uppercase
# Input: ['a','b'] → Output: ['A','B']
s = [x.upper() for x in ["a", "b"]]
print(s)

# Filter out vowels from a string
# Input: 'hello world' → Output: ['h','l','l',' ','w','r','l','d']
vowel = "aeiou"
str1 = "hello world"
s = [x for x in str1 if x not in vowel]
print(s)

# Create a list of lengths of given words
# Input: ['apple', 'banana'] → Output: [5,6]
s1 = ["apple", "banana"]
res = [len(x) for x in s1]
print(res)

# Flatten a 2D list
# Input: [[1, 2], [3, 4]] → Output: [1, 2, 3, 4]
input = [[1, 2], [3, 4]]
s = [x for y in input for x in y]
print(s)

# Get square of even numbers only
# Input: [1,2,3,4,5] → Output: [4, 16]
s = [x * x for x in range(6) if x % 2 == 0]
print(s)

# Extract digits from a string
# Input: 'abc123xyz' → Output: ['1','2','3']
digit = [x for x in "abc123xyz" if x.isdigit()]
print(digit)

# Create a list of tuples (number, square)
# Input: [1,2,3] → Output: [(1,1), (2,4), (3,9)]

res = [(i, i * i) for i in range(1, 11)]
print(res)

# Get words with length > 3
# Input: ['hi','hello','to','world'] → Output: ['hello','world']
words = ["hi", "hello", "to", "world"]
res = [x for x in words if len(x) > 3]
print(res)

# Filter a dictionary by keys using list comprehension
# Only include keys that start with 'p'
# Input: {'kiwi': 5,', 'orange': 10, 'apple': 13,
# 'bannana': 2,'papaya': 8}
# Output: {'papaya': 8}
dict1 = {"kiwi": 5, "orange": 10, "apple": 13, "banana": 2, "papaya": 8}
res = dict([(k, v) for k, v in dict1.items() if k.startswith("p")])
print(res)

# Reverse each word in a list
# Input: ['cat', 'dog'] → Output: ['tac', 'god']
input = ["cat", "dog"]
rev_word = [i[::-1] for i in input]
print(rev_word)

# Replace all negative numbers with 0
# Input: [-1, 2, -3, 4] → Output: [0, 2, 0, 4]
input = [-1, 2, -3, 4]
res = [0 if i < 0 else i for i in input]
print(res)

# Find common elements in two lists
# Input: [1,2,3], [2,3,4] → Output: [2,3],
list1, list2 = [1, 2, 3], [2, 3, 4]
res = [i for i in list1 if i in list2]
print(res)

# Capitalize first letter of each word
# Input: ['hello', 'world'] → Output: ['Hello', 'World']
input = ["hello", "world"]
res = [i.title() for i in input]
print(res)

# Transpose a matrix
# Ianput: [[1,2],[3,4]] → Output: [[1,3],[2,4]]
input = [[1, 2], [3, 4]]
res = [[row[i] for row in input] for i in range(len(input[0]))]
print(res)
