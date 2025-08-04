import pytest
from pydantic import ValidationError

from Week3.models import Product


@pytest.mark.parametrize(
    "quantity, price, expected",
    [
        (10, 5.0, 50.0),
        (0, 100.0, 0.0),
        (3, 33.33, 99.99),
        (1000_000, 1000.0, 1_000_000_000.0),
        (0, 0.01, 0.0),
    ],
)
def test_get_total_value(quantity, price, expected) -> None:
    """
    Tests the get_total_value method of the Product class.

    The test uses a parametrize decorator to run the test
    function multiple times with different inputs.
    """
    product = Product(
        product_id=1,
        product_name="Sample",
        category="Test",
        quantity=quantity,
        price=price,
    )
    assert product.get_total_value() == pytest.approx(expected, 0.01)


def test_product_should_raise_validation_error_on_negative_price() -> None:
    """
    Tests that creating a Product with a negative price raises a ValidationError.

    This test ensures that the Product model enforces the constraint that
    the price must be greater than zero, as defined in the Product class
    using Pydantic's Field validation.
    """

    with pytest.raises(ValidationError):
        Product(
            product_id=1,
            product_name="Sample",
            category="Test",
            quantity=10,
            price=-1.0,
        )
