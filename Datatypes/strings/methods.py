str = "hello"
str1 = "hello i am doing programming"

# using find() to find first occurrence of str2
print ("The first occurrence of str2 is at : ", end="")
print (str.find( str))

# using rfind() to find last occurrence of str2
print ("The last occurrence of str2 is at : ", end="")
print ( str.rfind( str) )

# using startswith() to find if str starts with str1 
if str1.startswith(str): 
        print ("str1 begins with : " + str) 
else : print ("str1 does not begin with : "+ str) 

# using endswith() to find if str ends with str1 
if str1.endswith(str): 
    print ("str1 ends with : " + str) 
else : 
    print ("str1 does not end with : " + str)

str="VANSH"
str1="adarsh"
if str.isupper() :
    print ("All characters in str are upper cased")
else : 
    print ("All characters in str are not upper cased")

# checking if all characters in str1 are lower cased
if str1.islower() :
    print ("All characters in str1 are lower cased")
else : 
    print ("All characters in str1 are not lower cased")


# Python code to demonstrate working of upper(), lower(), swapcase() and title()
str = "I am doing PROGRAMMING"

# Converting string into its lower case
str1 = str.lower()
print (" The lower case converted string is : " + str1)

# Converting string into its upper case
str2 = str1.upper()
print (" The upper case converted string is : " + str2)

# Converting string into its swapped case
str3 = str.swapcase()
print (" The swap case converted string is : " + str3)

# Converting string into its title case
str4 = str.title()
print (" The title case converted string is : " + str4)

# len() and count()
str = "geeksforgeeks is for geeks"
 
# Printing length of string using len()
print (" The length of string is : ", len(str));

# Printing occurrence of "geeks" in string
# Prints 2 as it only checks till 15th element
print (" Number of appearance of ""geeks"" is : ",end="")
print (str.count("geeks",0,15))


# isalpha(), isalnum(), isspace()
str = "geeksforgeeks"
str1 = "123"
 
# Checking if str has all alphabets 
if (str.isalpha()):
       print ("All characters are alphabets in str")
else : print ("All characters are not alphabets in str")

# Checking if str1 has all numbers
if (str1.isalnum()):
       print ("All characters are numbers in str1")
else : print ("All characters are not numbers in str1")

# Checking if str1 has all spaces
if (str1.isspace()):
       print ("All characters are spaces in str1")
else : print ("All characters are not spaces in str1")


# Python code to demonstrate working of 
# join()
str1 = ( "i", "love", "india" )

# using join() to join sequence str1 with str
print ("The string after joining is : ", end="")
print ( ''.join(str1))


# Python code to demonstrate working of 
# strip(), lstrip() and rstrip()
my_str = "---hello world---"

# using strip() to delete all '-'
print ( " String after stripping all '-' is : ", end="")
print ( my_str.strip('-') )

# using lstrip() to delete all trailing '-'
print ( " String after stripping all leading '-' is : ", end="")
print ( my_str.lstrip('-') )

# using rstrip() to delete all leading '-'
print ( " String after stripping all trailing '-' is : ", end="")
print ( my_str.rstrip('-') )

# Python code to demonstrate working of 
# min() and max()
str = "chourasia"

# using min() to print the smallest character
# prints 'e'
print ("The minimum value character is : " + min(str))

# using max() to print the largest character
# prints 's'
print ("The maximum value character is : " + max(str))


# Python code to demonstrate working of 
# replace()

str = "hyforhy is for hy"

str1 = "hy"
str2 = "hello"

# using replace() to replace str2 with str1 in str
# only changes 2 occurrences 
print ("The string after replacing strings is : ", end="")
print (str.replace( str1, str2, 2))