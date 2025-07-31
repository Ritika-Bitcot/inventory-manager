filename = "binaryfile.bin"

def write_binary_file() -> None:
    """
    Creates a binary file and writes multiple lines to it in binary mode.
    """
    try:
        with open(filename, "wb") as f:
            f.write(b"hello, my name is ritika chourasia\n")
            f.write(b"I live in Indore\n")
            f.write(b"I am working in bitcot\n")
        print("Binary file written successfully.")
    except PermissionError:
        print("You do not have permission to write to the binary file.")

def read_binary_file() -> None:
    """
    Reads and prints the entire binary content of the file.
    """
    try:
        with open(filename, "rb") as f:
            print("\nReading binary file:")
            print(f.read())
    except FileNotFoundError:
        print("The binary file was not found.")
    except PermissionError:
        print("You do not have permission to read the binary file.")

def modify_binary_file() -> None:
    """
    Opens the binary file in read-write mode ('rb+') and overwrites the beginning.
    Prints the content before modification.
    """
    try:
        with open(filename, "rb+") as file:
            content = file.read()
            print("\nBinary content before modification:")
            print(content)
            file.seek(0)
            file.write(b"Modified binary line.\n")
    except FileNotFoundError:
        print("The binary file was not found.")
    except PermissionError:
        print("You do not have permission to modify the binary file.")

def overwrite_binary_file() -> None:
    """
    Opens the file in write-read mode ('wb+'), which overwrites the file,
    writes a new line, and reads the content from the beginning.
    """
    try:
        with open(filename, "wb+") as file:
            file.write(b"Overwritten in wb+ mode.\n")
            file.seek(0)
            print("\nReading after overwriting in 'wb+':")
            print(file.read())
    except PermissionError:
        print("You do not have permission to write to the binary file.")

def append_read_binary_file() -> None:
    """
    Opens the file in append-read mode ('ab+'), appends a new line,
    then reads the entire content from the beginning.
    """
    try:
        with open(filename, "ab+") as file:
            file.write(b"Appended using ab+.\n")
            file.seek(0)
            print("\nReading full binary content after 'ab+':")
            print(file.read())
    except PermissionError:
        print("You do not have permission to append to the binary file.")

if __name__ == "__main__":
    write_binary_file()
    read_binary_file()
    modify_binary_file()
    # overwrite_binary_file()  # Uncomment if you want to overwrite completely
    append_read_binary_file()
