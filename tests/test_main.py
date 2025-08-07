from unittest.mock import MagicMock, patch

from Week3 import main


def test_main_success(capsys) -> None:
    """
    Tests that main.main() works as expected with a mock inventory, by patching
    the Inventory class and the setup_logger function. Verifies that the output
    contains all the expected lines.
    """
    mock_inventory = MagicMock()
    mock_inventory.load_from_csv.return_value = None
    mock_inventory.get_summary.return_value = {
        "total_products": 5,
        "total_quantity": 50,
        "hs_name": "Mock Product",
        "hs_amt": 1234.56,
        "total_value": 7890.12,
    }
    mock_inventory.generate_low_stock_report.return_value = None

    with patch("Week3.main.Inventory", return_value=mock_inventory), patch(
        "Week3.main.setup_logger"
    ):

        main.main()

    captured = capsys.readouterr()
    output = captured.out

    assert "INVENTORY SUMMARY DASHBOARD" in output
    assert "Total Products       : 5" in output
    assert "Total Quantity       : 50" in output
    assert "Highest Sale Product : Mock Product (₹1234.56)" in output
    assert "Total Inventory Value: ₹7890.12" in output


def test_main_exception(capsys) -> None:
    """
    Tests that main() logs and prints an error message when an exception occurs.
    """
    with patch(
        "Week3.main.Inventory", side_effect=Exception("Some error occurred")
    ), patch("Week3.main.setup_logger"):

        main.main()

    captured = capsys.readouterr()
    assert "Some error occurred" in captured.out
