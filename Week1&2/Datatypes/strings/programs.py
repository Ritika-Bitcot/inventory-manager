#Reverse string
s="Ritika Chourasia"
print("Reverse of string:",s[::-1])

#Check if a String is Palindrome
ans="Palindrome" if s==s[::-1] else "Not palindrome"
print(ans)

#Count the Number of Vowels in a String
vowel="aeiou"
print(sum(1 for i in s if i in vowel))

#Check if Two Strings are Anagrams
str1 = "listen"
str2 = "silent"

ans="Anagrams" if sorted(str1)==sorted(str2) else "Not Anagrams"
print(f'{str1} and {str2} are {ans}')

#Convert the First Letter of Each Word to Uppercase
s = "hello world from python"
print(s.title())
