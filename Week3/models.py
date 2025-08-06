from datetime import datetime
from typing import Optional

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, ConfigDict, Field, model_validator

# Registry
PRODUCT_CLASS_MAP = {}


def register_product_type(category: str):
    """
    Registers a product type with the given category.
    The category is converted to lower case to ensure that
    the mapping is case-insensitive.
    """

    def decorator(cls):
        """
        Decorator to register a product type with the given category.
        The category is converted to lower case to ensure that
        the mapping is case-insensitive.
        """
        PRODUCT_CLASS_MAP[category.lower()] = cls
        return cls

    return decorator


# Base Product
class Product(BaseModel):
    product_id: int = Field(..., gt=0)
    product_name: str = Field(..., min_length=3, max_length=50)
    category: Optional[str] = None
    quantity: int = Field(..., ge=0)
    price: float = Field(..., gt=0)

    model_config = ConfigDict(extra="forbid")

    def get_total_value(self) -> float:
        """
        Returns the total value of the product based on its price and quantity.
        """
        return self.price * self.quantity


# Subclasses
@register_product_type("food")
class FoodProduct(Product):
    category: str = "food"
    mfg_date: datetime
    expiry_date: datetime

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def check_expiry_after_mfg(self) -> Product:
        """
        Checks if the expiry date is after the manufacturing date.
        """

        if self.expiry_date <= self.mfg_date:
            raise ValueError("expiry_date must be after mfg_date")
        return self


@register_product_type("electronic")
class ElectronicProduct(Product):
    category: str = "electronic"
    purchase_date: datetime
    warranty_period: int = Field(..., ge=0)

    model_config = ConfigDict(extra="forbid")

    def get_warranty_end_date(self) -> datetime:
        """
        Calculates the warranty end date based on the purchase date.
        """
        return self.purchase_date + relativedelta(months=self.warranty_period)


@register_product_type("book")
class BookProduct(Product):
    category: str = "book"
    author: str = Field(..., min_length=3)
    publication_year: int = Field(..., ge=1000, le=datetime.now().year)

    model_config = ConfigDict(extra="forbid")
