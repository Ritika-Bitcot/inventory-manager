#string creation
string1='hello my name is Ritika'
string2="Hello I'am Ritika"
string3='''
My name is Ritika
I Live in Indore
currently working in bitcot
'''
print(string1,string2,string3)

# Python Program to Access characters of String
print(string1[2])
print(string2[6:11])
print(string3[::-1]) #reverse string
print(string1[::2])

# Python Program to Update character of a String

### there are following two ways
#1
list1 = list(string1)
list1[2] = 'p'
String2 = ''.join(list1)
print("\nUpdating character at 2nd Index: ")
print(String2)

#2
String3 = string1[0:2] + 'l' + string1[3:]
print(String3)


# Deleting a character of the String
string3 = string2[0:18] + string3[34:]
print("\nDeleting character at 2nd Index: ")
print(string3)

#delete entire String
s=''
del s


# Python Program for Formatting of Strings

# Default order
String1 = "{} {} {}".format('Geeks', 'For', 'Life')
print("Print String in default order: ")
print(String1)

# Positional Formatting
String1 = "{1} {0} {2}".format('Geeks', 'For', 'Life')
print("\nPrint String in Positional order: ")
print(String1)

# Keyword Formatting
String1 = "{l} {f} {g}".format(g='Geeks', f='For', l='Life')
print("\nPrint String in order of Keywords: ")
print(String1)