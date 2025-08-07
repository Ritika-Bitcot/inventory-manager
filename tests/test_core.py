from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import mock_open, patch

import pytest

from Week3.core import Inventory
from Week3.models import FoodProduct, Product


def test_create_valid_product_row(sample_product: Product) -> None:
    """Test creating a valid Product from a row dictionary."""
    inv = Inventory()
    row = {
        "product_id": str(sample_product.product_id),
        "product_name": sample_product.product_name,
        "category": sample_product.category,
        "quantity": str(sample_product.quantity),
        "price": str(sample_product.price),
    }
    product = inv.create_product_from_row(row)
    assert isinstance(product, Product)
    assert product.product_id == sample_product.product_id


def test_create_product_with_missing_field(caplog: pytest.LogCaptureFixture) -> None:
    """Test logging error when required fields are missing in row."""
    inv = Inventory()
    row = {"product_name": "Test"}
    with caplog.at_level("ERROR"):
        product = inv.create_product_from_row(row)
    assert product is None
    assert "Missing required field" in caplog.text


def test_create_product_with_wrong_type(caplog: pytest.LogCaptureFixture) -> None:
    """Test logging error when product_id cannot be converted to int."""
    inv = Inventory()
    row = {
        "product_id": "abc",
        "product_name": "Test",
        "category": "stationery",
        "quantity": "10",
        "price": "5.0",
    }
    with caplog.at_level("ERROR"):
        product = inv.create_product_from_row(row)
    assert product is None
    assert "Type error" in caplog.text


def test_create_product_unexpected_exception(caplog: pytest.LogCaptureFixture) -> None:
    """Test unexpected exception in create_product_from_row."""
    inv = Inventory()

    valid_row = {
        "product_id": "1",
        "product_name": "Pen",
        "category": "stationery",
        "quantity": "10",
        "price": "5.0",
    }

    with patch(
        "Week3.models.Product.__init__", side_effect=RuntimeError("unexpected failure")
    ):
        with caplog.at_level("ERROR"):
            product = inv.create_product_from_row(valid_row)

    assert product is None
    assert "Unexpected error processing row" in caplog.text
    assert "unexpected failure" in caplog.text


def test_load_valid_csv_file(tmp_path: Path, sample_product: Product) -> None:
    """Test loading a valid CSV file with one product."""
    inv = Inventory()
    file_path = tmp_path / "products.csv"
    file_content = (
        "product_id,product_name,category,quantity,price\n"
        f"{sample_product.product_id},{sample_product.product_name},"
        f"{sample_product.category},{sample_product.quantity},{sample_product.price}\n"
    )
    file_path.write_text(file_content)
    inv.load_from_csv(str(file_path))
    assert len(inv.products) == 1
    assert inv.products[0].product_name == sample_product.product_name


def test_load_missing_csv_file(caplog: pytest.LogCaptureFixture) -> None:
    """Test logging error when file does not exist."""
    inv = Inventory()
    with caplog.at_level("ERROR"):
        inv.load_from_csv("missing.csv")
    assert "not found" in caplog.text


def test_generate_low_stock_file(
    tmp_path: Path, inventory_with_products: Inventory
) -> None:
    """Test generating low stock report with some products under threshold."""
    file_path = tmp_path / "low_stock.txt"
    inventory_with_products.generate_low_stock_report(
        threshold=6, output_file=str(file_path)
    )
    content = file_path.read_text()
    assert "Milk" in content
    assert "Phone" in content


def test_generate_low_stock_report_with_mock_write(
    mocker, inventory_with_products
) -> None:
    """Test generate_low_stock_report using mock to capture write calls."""
    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)

    inventory_with_products.generate_low_stock_report(
        threshold=6, output_file="dummy.txt"
    )

    handle = mock_file()
    # Assert that write was called with expected content
    write_calls = [call.args[0] for call in handle.write.call_args_list]

    combined_content = "".join(write_calls)
    assert "Milk" in combined_content
    assert "Phone" in combined_content


def test_generate_low_stock_with_no_low_items(
    tmp_path: Path, inventory_with_products: Inventory, caplog: pytest.LogCaptureFixture
) -> None:
    """Test report when all products have sufficient stock."""
    file_path = tmp_path / "low_stock.txt"
    with caplog.at_level("INFO"):
        inventory_with_products.generate_low_stock_report(
            threshold=0, output_file=str(file_path)
        )
    content = file_path.read_text()
    assert "All products have sufficient stock" in content
    assert "No products found below" in caplog.text


def test_generate_low_stock_file_error(
    monkeypatch: Any,
    inventory_with_products: Inventory,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test logging error when file writing fails."""

    def raise_ioerror(*args, **kwargs):
        raise FileNotFoundError("Fake error")

    monkeypatch.setattr("builtins.open", raise_ioerror)
    with caplog.at_level("ERROR"):
        inventory_with_products.generate_low_stock_report()
    assert "not found" in caplog.text


def test_inventory_total_value(inventory_with_products: Inventory) -> None:
    """Test calculating total inventory value."""
    total = inventory_with_products.get_total_inventory()
    expected = sum(p.get_total_value() for p in inventory_with_products.products)
    assert total == expected


def test_inventory_summary_empty(caplog: pytest.LogCaptureFixture) -> None:
    """Test summary when inventory has no products."""
    inv = Inventory()
    with caplog.at_level("WARNING"):
        summary = inv.get_summary()
    assert summary["total_products"] == 0
    assert summary["total_quantity"] == 0
    assert summary["hs_name"] == "N/A"
    assert summary["total_value"] == 0.0
    assert "No valid (non-expired) products" in caplog.text


def test_inventory_summary_with_products(inventory_with_products: Inventory) -> None:
    """Test valid summary output with non-empty inventory."""
    summary = inventory_with_products.get_summary()
    assert summary["total_products"] > 0
    assert summary["total_quantity"] > 0
    assert summary["total_value"] > 0
    assert summary["hs_name"] != "N/A"
    assert summary["hs_amt"] > 0


def test_inventory_summary_with_expired_food() -> None:
    """Test that expired food products are excluded in summary."""
    inv = Inventory()
    expired = FoodProduct(
        product_id=1,
        product_name="Expired Milk",
        quantity=10,
        price=50.0,
        mfg_date=datetime.now() - timedelta(days=10),
        expiry_date=datetime.now() - timedelta(days=1),
    )
    inv.products.append(expired)
    summary = inv.get_summary()
    assert summary["total_products"] == 0
    assert summary["total_quantity"] == 0


def test_load_csv_with_mock_open() -> None:
    """Test loading CSV using mock_open to avoid real files."""
    csv_data = (
        "product_id,product_name,category,quantity,price\n1,Pen,stationery,10,5.0\n"
    )
    inv = Inventory()
    with patch("builtins.open", mock_open(read_data=csv_data)) as mock_file:
        inv.load_from_csv("dummy.csv")
    assert len(inv.products) == 1
    mock_file.assert_called_once_with("dummy.csv", newline="")


def test_create_product_with_validation_error(caplog: pytest.LogCaptureFixture) -> None:
    """Test logging validation error when date format is invalid."""
    inv = Inventory()
    row = {
        "product_id": "1",
        "product_name": "Milk",
        "category": "food",
        "quantity": "10",
        "price": "5.0",
        "mfg_date": "not-a-date",
        "expiry_date": "2025-01-01",
    }
    with caplog.at_level("ERROR"):
        product = inv.create_product_from_row(row)
    assert product is None
    assert "Validation error" in caplog.text


def test_summary_with_zero_total_quantity(caplog: pytest.LogCaptureFixture) -> None:
    """Test get_summary logs warning when total quantity is zero."""
    inv = Inventory()

    inv.products = [
        Product(
            product_id=1,
            product_name="Item1",
            category="stationery",
            quantity=0,
            price=10.0,
        ),
        Product(
            product_id=2,
            product_name="Item2",
            category="stationery",
            quantity=0,
            price=20.0,
        ),
    ]

    with caplog.at_level("WARNING"):
        summary = inv.get_summary()

    assert summary["total_quantity"] == 0
    assert "Total quantity is zero — all products may be out of stock." in caplog.text


def test_create_product_with_extra_field(caplog: pytest.LogCaptureFixture) -> None:
    """Test logging validation error when extra unexpected field is present."""
    inv = Inventory()
    row = {
        "product_id": "1",
        "product_name": "Milk",
        "category": "food",
        "quantity": "10",
        "price": "5.0",
        "mfg_date": "2024-01-01",
        "expiry_date": "2025-01-01",
        "extra_field": "unexpected",
    }
    with caplog.at_level("ERROR"):
        product = inv.create_product_from_row(row)
    assert product is None
    assert "Validation error in row" in caplog.text


def test_load_csv_with_invalid_row(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Test that invalid rows in CSV do not get added to products."""
    file_path = tmp_path / "products.csv"
    file_path.write_text(
        "product_id,product_name,category,quantity,price\n"
        "1,Valid,stationery,10,5.0\n"
        "2,Invalid,stationery,not_a_number,5.0\n"
    )
    inv = Inventory()
    with caplog.at_level("ERROR"):
        inv.load_from_csv(str(file_path))
    assert len(inv.products) == 1
    assert "Type error" in caplog.text


def test_summary_max_raises_error(
    caplog: pytest.LogCaptureFixture, inventory_with_products: Inventory
) -> None:
    """Test logging error if max() fails while calculating highest sale."""
    with patch("builtins.max", side_effect=Exception("max failed")):
        with caplog.at_level("ERROR"):
            inventory_with_products.get_summary()
    assert "Error calculating highest sale" in caplog.text


def test_load_csv_with_exception(caplog: pytest.LogCaptureFixture) -> None:
    """Test logging unexpected exception during file reading."""
    inv = Inventory()
    with patch("builtins.open", side_effect=ValueError("fake error")):
        with caplog.at_level("ERROR"):
            inv.load_from_csv("file.csv")
    assert "fake error" in caplog.text


def test_generate_low_stock_generic_exception(
    monkeypatch: Any,
    inventory_with_products: Inventory,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test logging generic error during report file writing."""

    def raise_generic(*args: Any, **kwargs: Any) -> None:
        raise Exception("Something went wrong")

    monkeypatch.setattr("builtins.open", raise_generic)
    with caplog.at_level("ERROR"):
        inventory_with_products.generate_low_stock_report()
    assert "Error writing low stock report" in caplog.text


def test_food_product_with_valid_dates_in_summary() -> None:
    """
    Tests that a food product with valid dates is included in the summary.
    """
    inv = Inventory()
    valid_food = FoodProduct(
        product_id=10,
        product_name="Fresh Milk",
        quantity=10,
        price=5.0,
        mfg_date=datetime.now() - timedelta(days=1),
        expiry_date=datetime.now() + timedelta(days=10),
    )
    inv.products.append(valid_food)
    summary = inv.get_summary()
    assert summary["total_products"] == 1
    assert summary["total_quantity"] == 10


def test_low_stock_excludes_expired_food(tmp_path: Path) -> None:
    """
    Tests that expired food products are excluded from the low stock report.
    """
    inv = Inventory()
    expired = FoodProduct(
        product_id=2,
        product_name="Expired Bread",
        quantity=2,
        price=20.0,
        mfg_date=datetime.now() - timedelta(days=10),
        expiry_date=datetime.now() - timedelta(days=1),
    )
    inv.products.append(expired)

    file_path = tmp_path / "report.txt"
    inv.generate_low_stock_report(threshold=5, output_file=str(file_path))
    content = file_path.read_text()
    assert "Expired Bread" not in content
