import csv

def data_processing(filename: str)->None:
    """
    Process the given CSV file, print out the total value of each row after validation.
    
    Args:
        filename (str): The path to the CSV file
    
    Raises:
        FileNotFoundError: If the file does not exist
        ZeroDivisionError: If the quantity is zero
    """
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header

            for i,row in enumerate(reader,start=2):
                try:
                    name=str(row[0])
                    price=float(row[1])
                    quantity=int(row[2])
                    
                except ValueError:
                    print(f"Error in row {i}: Invalid data format.")
                except KeyError:
                    print(f"Error in row {i}: Missing column.")
                    
                if quantity == 0:
                    raise ZeroDivisionError(f"Row {i}: Quantity is zero")
                
                total_value = price * quantity
                print(f"Row {i}: Name: {name}, Price: {price:.2f}, Quantity: {quantity}")
                print(f"Total Value: ₹{total_value:.2f}\n")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except ZeroDivisionError as e:
        print(f"Error: {e}")
data_processing("data.csv")