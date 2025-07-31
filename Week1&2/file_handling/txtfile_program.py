filename = "test_textfile.txt"

def create_file() -> None:
    """
    Creates a text file with the given filename and writes multiple lines to it.
    """
    try:
        with open(filename, "x") as f:
            f.write("hello, my name is ritika chourasia\n")
            f.writelines(["I live in Indore\n", "I am working in bitcot\n"])
        print("File created successfully.")
    except FileExistsError:
        print("File already exists.")
    except PermissionError:
        print("You do not have permission to create the file.")

def read_file() -> None:
    """
    Reads and prints the entire content of the specified text file.
    """
    try:
        with open(filename, "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
    except PermissionError:
        print("You do not have permission to read the file.")

def readlines_file() -> None:
    """
    Reads the file and prints the entire content as a list of lines.
    The lines are read using the readlines() method of the file object.
    """
    try:
        with open(filename, "r") as f:
            print(f.readlines())
    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
    except PermissionError:
        print("You do not have permission to read the file.")

def readline_using_forloop() -> None:
    """
    Reads the file line by line and prints each line.
    """
    try:
        with open(filename, "r") as f:
            for line in f:
                print(line, end="")
    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
    except PermissionError:
        print("You do not have permission to read the file.")

def append_file() -> None:
    """
    Appends a new line to the end of the file.
    """
    try:
        with open(filename, "a") as f:
            f.write("I am learning python\n")
    except PermissionError:
        print("You do not have permission to write to the file.")

def read_write_mode() -> None:
    """
    Opens the file in read-write mode and reads the content.
    Then, moves the file pointer to the beginning and writes a new line.
    Prints the current position of the file pointer and reads the content again.
    """
    try:
        with open(filename, "r+") as f:
            print(f.read())
            f.seek(0)
            f.write("Hello, my name is Ritika Chourasia")
            print(f.tell())
            print(f.read())
    except FileNotFoundError:
        print(f"The file '{filename}' was not found. Please check the file path.")
    except PermissionError:
        print(f"You do not have permission to read and write to the file '{filename}'.")

def write_read_mode() -> None:
    """
    Opens the file in write-read mode and writes a new line.
    Then, moves the file pointer to the beginning and reads the content.
    Prints the content of the file.
    """
    try:
        with open(filename, "w+") as f:
            f.write("W+ mode overwrites content.\n")
            f.seek(0)
            print("\nReading after writing in 'w+':")
            print(f.read())
    except PermissionError:
        print(f"You do not have permission to write to the file '{filename}'.")

def append_read_mode() -> None:
    """
    Opens the file in append-read mode and appends a new line.
    Then, moves the file pointer to the beginning and reads the content.
    Prints the content of the file.
    """
    try:
        with open(filename, "a+") as f:
            f.write("A+ mode appends content.\n")
            f.seek(0)
            print("\nReading after appending in 'a+':")
            print(f.read())
    except PermissionError:
        print(f"You do not have permission to write to the file '{filename}'.")

if __name__ == "__main__":
    create_file()
    read_file()
    readlines_file()
    readline_using_forloop()
    append_file()
    read_write_mode()
    # write_read_mode()   # Uncomment if you want to overwrite completely
    append_read_mode()

    print("\nProgram completed successfully.")