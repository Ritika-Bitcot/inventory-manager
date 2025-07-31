# Function to find majority element
from collections import Counter

def majority(arr):
    freq = Counter(arr)

    size = len(arr)
    for k,v in freq.items():
         if (v > (size/2)):
             print(k)
             return
    print('None')

arr = [3,3,4,2,4,4,2,4,4] 
majority(arr)

# Function to find common elements in three
# sorted arrays
from collections import Counter

def commonElement(ar1,ar2,ar3):
    ar1 = Counter(ar1)
    ar2 = Counter(ar2)
    ar3 = Counter(ar3)
   
    result = dict(ar1.items() & ar2.items() & ar3.items())
    print(list(result.keys()))

ar1 = [1, 5, 10, 20, 40, 80]
ar2 = [6, 7, 20, 80, 100]
ar3 = [3, 4, 15, 20, 30, 70, 80, 120]
commonElement(ar1,ar2,ar3)


# Python code to convert  list of tuples into dictionary    
tups = [("akash", [10,13,56]), ("gaurav", [12,"hello"]), ("anand", 14), 
     ("suraj", 20), ("akhil", 25), ("ashish", 30)]
dictionary = {}
dic1=dict(tups)
print(dic1)

# Group words with same length
words = ["hi", "code", "python", "a", "go"]
grouped = {}
for word in words:
    length = len(word)
    grouped.setdefault(length, []).append(word)
print(grouped)

# Swap key and values in dictionary
d = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in d.items()}
print(inverted)
