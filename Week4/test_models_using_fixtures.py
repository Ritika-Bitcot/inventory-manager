from datetime import datetime, timedelta

# ----------------------------
# Inventory Core Functionality
# ----------------------------


def test_inventory_stores_products_correctly(inventory_with_products) -> None:
    """
    Tests that the inventory stores products correctly.
    """
    # Act
    total_products = len(inventory_with_products.products)

    # Assert
    assert total_products == 4  # Pen, Milk, Phone, Book


def test_get_total_inventory_value(inventory_with_products) -> None:
    """
    Tests the get_total_inventory method of Inventory.
    """
    expected_value = (
        10 * 5.0 + 5 * 20.0 + 2 * 1000.0 + 7 * 800.0  # Pen  # Milk  # Phone  # Book
    )

    # Act
    total_value = inventory_with_products.get_total_inventory()

    # Assert
    assert total_value == expected_value


# ----------------------------
# Inventory Summary Behavior
# ----------------------------


def test_get_summary_excludes_expired_food_product(
    inventory_with_products, food_product
) -> None:
    """
    Tests that the get_summary method of Inventory excludes expired food products.
    """
    # Arrange
    food_product.expiry_date = datetime.now() - timedelta(days=1)  # expire milk

    # Act
    summary = inventory_with_products.get_summary()

    # Assert
    assert summary["total_products"] == 3  # Milk excluded
    assert summary["hs_name"] != "Milk"


def test_inventory_summary_includes_book(inventory_with_products) -> None:
    """
    Tests that the inventory summary includes the book product.
    """
    # Act
    summary = inventory_with_products.get_summary()

    # Assert
    assert summary["total_products"] == 4
    assert summary["total_quantity"] >= 7


# ----------------------------
# Fixture-Specific Tests
# ----------------------------


def test_book_product_fixture(book_product) -> None:
    """
    Tests that the book_product fixture has the correct author and total value.
    """
    # Act
    total_value = book_product.get_total_value()

    # Assert
    assert book_product.author == "Robert Martin"
    assert total_value == 7 * 800.0
