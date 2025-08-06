import builtins
import logging
from datetime import datetime, timedelta
from unittest.mock import patch

from Week3.core import Inventory
from Week3.models import FoodProduct, Product


def test_create_product_from_row_missing_field(inventory_with_products) -> None:
    """
    Tests that a product can't be created from a row that is missing a required field.
    """
    row = {
        "product_name": "Missing ID",
        "category": "stationery",
        "quantity": "10",
        "price": "5.0",
    }
    product = inventory_with_products.create_product_from_row(row)
    assert product is None


def test_create_product_from_row_invalid_type(inventory_with_products) -> None:
    """
    Tests that a product can't be created from a row with invalid type.
    """
    row = {
        "product_id": "1",
        "product_name": "Invalid Price",
        "category": "stationery",
        "quantity": "10",
        "price": "not-a-number",
    }
    product = inventory_with_products.create_product_from_row(row)
    assert product is None


def test_create_product_from_row_validation_error(inventory_with_products) -> None:
    """
    Tests that a product can't be created from a row that doesn't pass validation rules.
    """

    row = {
        "product_id": "0",
        "product_name": "Invalid Product",
        "category": "stationery",
        "quantity": "10",
        "price": "5.0",
    }
    product = inventory_with_products.create_product_from_row(row)
    assert product is None


def test_create_product_from_row_key_error(inventory_with_products, caplog) -> None:
    """
    Tests KeyError is logged when a required key is missing from the row.
    """
    row = {
        "product_name": "No ID Key",
        "category": "stationery",
        "quantity": "10",
        "price": "5.0",
    }
    with caplog.at_level(logging.ERROR):
        product = inventory_with_products.create_product_from_row(row)

    assert product is None
    assert "Missing required field" in caplog.text


def test_load_from_csv_file_not_found(inventory_with_products, caplog) -> None:
    """
    Tests that an error is logged when trying to load a CSV file that doesn't exist.
    """
    with caplog.at_level(logging.ERROR):
        inventory_with_products.load_from_csv("non_existent_file.csv")
    assert any(
        "CSV file 'non_existent_file.csv' not found." in rec.message
        for rec in caplog.records
    )


def test_load_from_csv_with_invalid_row(
    tmp_path, inventory_with_products, caplog
) -> None:
    """
    Tests that an error is logged when trying to load a CSV
    file with an invalid row (missing required field).
    """
    csv_content = (
        "product_id,product_name,category,quantity,price\n"
        "1,Valid Product,stationery,10,5.0\n"
        ",Invalid Product,stationery,10,5.0\n"
    )

    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    with caplog.at_level(logging.ERROR):
        inventory_with_products.load_from_csv(str(csv_file))

    # Match actual error pattern from core.py
    assert any("Type error in row" in rec.message for rec in caplog.records)


def test_load_from_csv_with_validation_error(
    tmp_path, inventory_with_products, caplog
) -> None:
    csv_content = (
        "product_id,product_name,category,quantity,price\n"
        "0,Invalid Product,stationery,10,5.0\n"
    )
    csv_file = tmp_path / "validation_test.csv"
    csv_file.write_text(csv_content)

    with caplog.at_level(logging.ERROR):
        inventory_with_products.load_from_csv(str(csv_file))

    # Accept either type or validation error prefix
    assert any(
        phrase in caplog.text.lower()
        for phrase in ["type error in row", "validation error in row"]
    )


def test_generate_low_stock_report_file_not_found(
    inventory_with_products, tmp_path, caplog
) -> None:
    """
    Tests that an error is logged when trying to generate a low stock
    report to a file location that doesn't exist. The test mocks the
    `open` function to raise a `FileNotFoundError` and verifies that
    the appropriate error message is logged.
    """

    def raise_fnf(*args, **kwargs) -> None:
        """
        A function that raises a FileNotFoundError when called.
        """
        raise FileNotFoundError()

    output_file = tmp_path / "output.txt"
    original_open = builtins.open
    try:
        builtins.open = raise_fnf
        with caplog.at_level(logging.ERROR):
            inventory_with_products.generate_low_stock_report(
                output_file=str(output_file)
            )
        assert any("Output directory for file" in rec.message for rec in caplog.records)
    finally:
        builtins.open = original_open


def test_generate_low_stock_report_file_not_found_explicit(
    inventory_with_products, caplog
) -> None:
    with patch("builtins.open", side_effect=FileNotFoundError("Cannot open file")):
        with caplog.at_level(logging.ERROR):
            # Use keyword arguments to avoid positional conflict
            inventory_with_products.generate_low_stock_report(
                threshold=0, output_file="dummy_path.txt"
            )
        assert "Output directory for file" in caplog.text


def test_generate_low_stock_report_generic_exception(
    inventory_with_products, caplog
) -> None:
    def raise_exception(*args, **kwargs):
        raise Exception("Some unexpected error")

    original_open = builtins.open
    builtins.open = raise_exception
    try:
        with caplog.at_level(logging.ERROR):
            inventory_with_products.generate_low_stock_report("any_path.txt")
        assert "Error writing low stock report" in caplog.text
    finally:
        builtins.open = original_open


def test_get_summary_empty_inventory(caplog) -> None:
    """
    Tests that a warning is logged when generating a summary from an empty inventory.
    """
    inventory = Inventory()
    with caplog.at_level(logging.WARNING):
        summary = inventory.get_summary()
    assert summary["total_products"] == 0
    assert "Summary values will all be zero" in caplog.text


def test_get_summary_all_expired_food_products(caplog) -> None:
    """
    Tests that a warning is logged when generating a summary from an inventory
    where all FoodProducts are expired.
    """
    inventory = Inventory()
    expired_food = FoodProduct(
        product_id=10,
        product_name="Expired Milk",
        quantity=5,
        price=20.0,
        mfg_date=datetime.now() - timedelta(days=10),
        expiry_date=datetime.now() - timedelta(days=1),
    )
    inventory.products.append(expired_food)

    with caplog.at_level(logging.WARNING):
        summary = inventory.get_summary()

    assert summary["total_products"] == 0
    assert "Summary values will all be zero" in caplog.text


def test_get_summary_total_quantity_zero(caplog) -> None:
    """
    Tests that a warning is logged when generating a summary from an inventory
    where all products have zero quantity.
    """
    inventory = Inventory()
    product = Product(
        product_id=1, product_name="Zero Qty", quantity=0, price=100.0, category="misc"
    )
    inventory.products.append(product)

    with caplog.at_level(logging.WARNING):
        summary = inventory.get_summary()

    assert summary["total_quantity"] == 0
    assert "all products may be out of stock" in caplog.text


def test_get_summary_highest_sale_exception(
    monkeypatch, inventory_with_products, caplog
) -> None:
    """
    Tests that a summary still contains valid data when an error is raised while
    calculating the highest sale. The exception is logged at the ERROR level.
    """

    def raise_exc(*args, **kwargs):
        raise Exception("max error")

    monkeypatch.setattr("builtins.max", raise_exc)

    with caplog.at_level(logging.ERROR):
        summary = inventory_with_products.get_summary()

    assert summary["hs_name"] == "N/A"
    assert summary["hs_amt"] == 0.0
    assert "Error calculating highest sale" in caplog.text


def test_create_product_from_row_validation_error_explicit(
    inventory_with_products,
) -> None:
    # Supply a row that triggers ValidationError,
    # e.g. product_id = 0 (which fails pydantic validation)
    row = {
        "product_id": "0",
        "product_name": "Invalid Product",
        "category": "stationery",
        "quantity": "10",
        "price": "5.0",
    }
    product = inventory_with_products.create_product_from_row(row)
    assert product is None


def test_load_from_csv_raises_error_outside_loop(
    inventory_with_products, tmp_path, caplog
) -> None:
    # Patch open to simulate an error during reading (outside row processing)
    with patch("builtins.open", side_effect=ValueError("Read error")):
        with caplog.at_level(logging.ERROR):
            inventory_with_products.load_from_csv(str(tmp_path / "dummy.csv"))
        assert "Read error" in caplog.text


def test_generate_low_stock_report_file_not_found_and_other_errors(
    inventory_with_products, caplog
) -> None:
    # Patch open to raise FileNotFoundError and other exceptions explicitly
    with patch("builtins.open", side_effect=FileNotFoundError("Cannot open file")):
        with caplog.at_level(logging.ERROR):
            inventory_with_products.generate_low_stock_report(output_file="dummy.txt")
        assert "Output directory for file" in caplog.text

    def raise_other_exc(*args, **kwargs):
        raise RuntimeError("Other error")

    with patch("builtins.open", side_effect=raise_other_exc):
        with caplog.at_level(logging.ERROR):
            inventory_with_products.generate_low_stock_report(output_file="dummy.txt")
        assert "Error writing low stock report" in caplog.text
