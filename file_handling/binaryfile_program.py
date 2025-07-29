filename="binaryfile.bin"

with open(filename,"wb") as f:
    f.write(b"hello, my name is ritika chourasia\n")
    f.write(b"I live in Indore\n")
    f.write(b"I am working in bitcot\n")

with open(filename,"rb") as f:
    print(f.read())

with open(filename, "rb+") as file:
    content = file.read()
    print("\nBinary content before modification:")
    print(content)
    file.seek(0)
    file.write(b"Modified binary line.\n")

# with open(filename, "wb+") as file:
#     file.write(b"Overwritten in wb+ mode.\n")
#     file.seek(0)
#     print("\nReading after writing in 'wb+':")
#     print(file.read())

with open(filename, "ab+") as file:
    file.write(b"Appended using ab+.\n")
    file.seek(0)
    print("\nReading full binary content after ab+:")
    print(file.read())
