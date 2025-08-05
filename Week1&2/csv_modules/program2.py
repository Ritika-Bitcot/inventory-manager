import csv


def read_csv_with_dictreader() -> None:
    """
    Reads a CSV file using DictReader and prints the values of each row.
    The CSV file is expected to have the following columns: id, name, email.
    """
    try:
        with open("contacts.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                print(f"ID: {row['id']}", end=" ")
                print(f"Name: {row['name']}", end=" ")
                print(f" Email: {row['email']}")
        print()
    except FileNotFoundError:
        print("Error: The file 'contacts.csv' was not found.")
    except KeyError as e:
        print(f"Error: The CSV file is missing a required column: {e}")
    except csv.Error as e:
        print(f"Error: An error occurred while reading the CSV file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def write_csv_with_dictwriter() -> None:
    """
    Writes a list of dictionaries to a CSV file using DictWriter.
    The dictionaries must have the following keys: id, name, email.
    The CSV file is expected to have the same columns.
    """
    data = [
        {"id": 101, "name": "David", "email": "david@example.com"},
        {"id": 102, "name": "Eva", "email": "eva@example.com"},
        {"id": 103, "name": "Frank", "email": "frank@example.com"},
    ]

    try:
        with open("contacts.csv", "w", newline="") as f:
            fieldnames = ["id", "name", "email"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            print("Data written to contacts.csv")

    except FileNotFoundError:
        print("The file was not found. Please check the file path.")

    except PermissionError:
        print("You do not have permission to write to the file.")

    except csv.Error as e:
        print(f"An error occurred while writing to the CSV file: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    write_csv_with_dictwriter()
    read_csv_with_dictreader()
