import csv


def write_csv_with_writer() -> None:
    """
    Writes data to a csv file using csv.writer.
    """
    try:
        with open("people.csv", "w", newline="") as f:
            writer = csv.writer(f)
            data = [
                ["name", "age", "city"],
                ["Alice", 25, "New York"],
                ["David", 29, "Chicago"],
                ["Eva", 35, "Houston"],
                ["Frank", 40, "Boston, MA"],
            ]
            writer.writerows(data)
            print("Data written to people.csv")

    except FileNotFoundError:
        print("File not found.")

    except PermissionError:
        print("Permission denied. Cannot write to file.")

    except Exception as e:
        print(f"An error occurred: {e}")


def read_csv_with_reader() -> None:
    """
    Reads data from a CSV file and prints the headers and each row's contents.
    """
    try:
        with open("people.csv", "r", newline="") as f:
            reader = csv.reader(f)
            headers = next(reader)
            print("Headers:", headers)
            for row in reader:
                print(f"Name: {row[0]}, Age: {row[1]}, City: {row[2]}")
            print()

    except FileNotFoundError:
        print("File not found.")

    except csv.Error as e:
        print(f"CSV error: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    read_csv_with_reader()
    write_csv_with_writer()
