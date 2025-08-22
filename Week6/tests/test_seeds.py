from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from api import seed
from click.testing import CliRunner, Result
from pytest_mock import MockerFixture


@pytest.fixture
def fake_csv_content() -> str:
    """
    Return fake CSV content to simulate product data.
    """
    return (
        "product_name,category,quantity,price,mfg_date,expiry_date,purchase_date,"
        "warranty_period,author,publication_year\n"
        "Milk,food,10,5.5,2024-01-01,2024-12-31,,,,,\n"
        "Laptop,electronic,2,50000,,,2023-01-01,24,,,\n"
        "Python 101,book,5,399,,,,,John Doe,2020\n"
    )


@pytest.fixture
def mock_open_csv(mocker: MockerFixture, fake_csv_content: str):
    """
    Patch builtins.open to return fake CSV content.
    """
    return mocker.patch("builtins.open", mocker.mock_open(read_data=fake_csv_content))


@pytest.fixture
def mock_db_session(mocker: MockerFixture):
    """
    Patch db.session and db.create_all with a MagicMock to avoid real DB operations.
    """
    session = mocker.MagicMock()
    mocker.patch.object(seed.db, "session", session)
    mocker.patch.object(seed.db, "create_all", return_value=None)
    return session


def test_create_product_from_row_food() -> None:
    """
    Ensure create_product_from_row returns a valid FoodProduct.
    """
    row = {
        "product_name": "Milk",
        "category": "food",
        "quantity": "10",
        "price": "5.5",
        "mfg_date": "2024-01-01",
        "expiry_date": "2024-12-31",
    }
    product = seed.create_product_from_row(row)
    assert product is not None
    assert product.product_name == "Milk"
    assert product.quantity == 10
    assert isinstance(product.mfg_date, date)


def test_create_product_from_row_electronic() -> None:
    """
    Ensure create_product_from_row returns a valid ElectronicProduct.
    """
    row = {
        "product_name": "Laptop",
        "category": "electronic",
        "quantity": "2",
        "price": "50000",
        "purchase_date": "2023-01-01",
        "warranty_period": "24",
    }
    product = seed.create_product_from_row(row)
    assert product is not None
    assert product.product_name == "Laptop"
    assert product.warranty_period == 24


def test_create_product_from_row_book() -> None:
    """
    Ensure create_product_from_row return a valid BookProduct.
    """
    row = {
        "product_name": "Python 101",
        "category": "book",
        "quantity": "5",
        "price": "399",
        "author": "John Doe",
        "publication_year": "2020",
    }
    product = seed.create_product_from_row(row)
    assert product is not None
    assert product.author == "John Doe"


def test_create_product_from_row_unknown_category(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Ensure unknown categories are skipped and a message is printed.
    """
    row = {"product_name": "Unknown", "category": "toys"}
    product = seed.create_product_from_row(row)
    assert product is None
    captured = capsys.readouterr()
    assert "Skipping unknown category" in captured.out


def test_create_product_from_row_invalid_data(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Ensure invalid row data is handled gracefully and returns None.
    """
    row = {
        "product_name": "Milk",
        "category": "food",
        "quantity": "abc",  # invalid int
        "price": "5.5",
        "mfg_date": "2024-01-01",
        "expiry_date": "2024-12-31",
    }
    product = seed.create_product_from_row(row)
    assert product is None
    captured = capsys.readouterr()
    assert "Error creating product" in captured.out


def test_seed_db_success(
    mock_open_csv, mock_db_session, mocker: MockerFixture, tmp_path: Path
) -> None:
    """
    Ensure seed_db inserts valid rows successfully.
    """
    fake_path = tmp_path / "products.csv"
    fake_path.write_text(
        "product_name,category,quantity,price,mfg_date,expiry_date\n"
        "Milk,food,10,5.5,2024-01-01,2024-12-31\n"
    )
    mocker.patch("api.seed.CSV_FILE", str(fake_path))

    runner = CliRunner()
    with seed.app.app_context():
        result: Result = runner.invoke(seed.seed_db)

    assert result.exit_code == 0
    assert "Database seeded successfully" in result.output
    assert mock_db_session.add.called
    assert mock_db_session.commit.called


def test_seed_db_missing_file(mocker: MockerFixture) -> None:
    """
    Ensure seed_db handles missing CSV file gracefully.
    """
    mocker.patch("api.seed.CSV_FILE", "/nonexistent/path.csv")

    runner = CliRunner()
    with seed.app.app_context():
        result: Result = runner.invoke(seed.seed_db)

    assert "CSV file not found" in result.output


def test_seed_db_skips_invalid_rows(
    mock_db_session, mocker: MockerFixture, tmp_path: Path
) -> None:
    """
    Ensure invalid rows are skipped and a message is printed.
    """
    csv_content = (
        "product_name,category,quantity,price,mfg_date,expiry_date\n"
        "Milk,food,abc,5.5,2024-01-01,2024-12-31\n"
    )
    fake_path = tmp_path / "products.csv"
    fake_path.write_text(csv_content)
    mocker.patch("api.seed.CSV_FILE", str(fake_path))

    runner = CliRunner()
    with seed.app.app_context():
        result: Result = runner.invoke(seed.seed_db)

    assert "Skipping row 1" in result.output


def test_cli_command_registered() -> None:
    """
    Ensure seed-db command is registered with Flask CLI.
    """
    assert "seed-db" in seed.app.cli.commands
