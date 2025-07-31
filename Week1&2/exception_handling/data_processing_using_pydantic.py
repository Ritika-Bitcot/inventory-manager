import csv
from pydantic import BaseModel,Field, field_validator, ValidationError
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

class Product(BaseModel):
    """
    Validates each row of the CSV:
    - name: str
    - price: positive Decimal rounded to 2 decimal places
    - quantity: non-negative integer
    """

    name: str
    price: Decimal=Field(..., gt=0)
    quantity: int=Field(..., gt=0)

    @field_validator("price", mode="before")
    @classmethod
    def round_price(cls, v: str)->Decimal:
        """
        Rounds price to 2 decimal places before validation.
        Raises ValueError if not a valid decimal.
        """
        try:
            return Decimal(str(v)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except (InvalidOperation, ValueError):
            raise ValueError("Price must be a valid decimal number with up to 2 decimal places.")


    
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
            reader = csv.DictReader(file)
            for i, row in enumerate(reader, start=2):
                try:
                    item = Product(**row)
                    print(item)
                    total = float(item.price) * item.quantity
                    print(f"Row {i}: Name: {item.name}, Price: {item.price}, Quantity: {item.quantity}")
                    print(f"Total Value: ₹{total:.2f}\n")
                except ValidationError as ve:
                    print(f"Row {i}: Validation Error")
                    for error in ve.errors():
                        print(f" - {error['loc'][0]}: {error['msg']}")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    
    except ZeroDivisionError:
        print(f"Row {i}: Quantity is zero")

if __name__ == "__main__":
    data_processing("data.csv")