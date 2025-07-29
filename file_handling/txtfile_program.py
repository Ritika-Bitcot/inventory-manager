filename="test_textfile.txt"

with open(filename,"w") as f:
    f.write("hello, my name is ritika chourasia\n")
    f.writelines(["I live in Indore\n","I am working in bitcot\n"])

with open(filename,"r") as f:
    print(f.read())

with open(filename,"r") as f:
    print(f.readlines())

with open(filename,"r") as f:
    for line in f:
        print(line)

with open(filename,"a") as f:
    f.write("I am learning python\n")

with open(filename,"r+") as f:
    print(f.read())
    f.seek(0)
    f.write("Hello, my name is Ritika Chourasia")
    print(f.tell())
    print(f.read())

# with open(filename, "w+") as f:
#     f.write("W+ mode overwrites content.\n")
#     f.seek(0)
#     print("\nReading after writing in 'w+':")
#     print(f.read())

with open(filename,'a+') as f:
    f.seek(35)
    f.write("Added using a+ mode.\n")
    f.seek(0)
    print(f.read())


