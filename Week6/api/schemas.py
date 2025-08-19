from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ProductBase(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., gt=0)

    @field_validator("category")
    def validate_category(cls, v) -> str:
        """
        Validate the category field of the ProductBase model.

        The category should be one of 'food', 'electronic', or 'book'.
        The category is case-insensitive, and will be converted to lowercase
        before validation.

        Args:
            v (str): The value of the category field.

        Returns:
            str: The validated and normalized category value.

        Raises:
            ValueError: If the category is invalid.
        """
        allowed = {"food", "electronic", "book"}
        if v.lower() not in allowed:
            raise ValueError(f"Invalid category: {v}. Must be one of {allowed}")
        return v.lower()


class FoodProductCreate(ProductBase):
    mfg_date: date
    expiry_date: date


class ElectronicProductCreate(ProductBase):
    purchase_date: date
    warranty_period: int = Field(..., ge=0)  # in months


class BookProductCreate(ProductBase):
    author: str = Field(..., min_length=1)
    publication_year: int = Field(..., ge=0)


# Union type for POST
ProductCreate = (FoodProductCreate, ElectronicProductCreate, BookProductCreate)


class ProductUpdate(BaseModel):
    product_name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, gt=0)

    mfg_date: Optional[date] = None
    expiry_date: Optional[date] = None
    purchase_date: Optional[date] = None
    warranty_period: Optional[int] = None
    author: Optional[str] = None
    publication_year: Optional[int] = None

    @field_validator("category")
    def validate_category(cls, v) -> str:
        """
        Validate the category field of the ProductUpdate model.

        The category should be one of 'food', 'electronic', or 'book'.
        The category is case-insensitive, and will be converted to lowercase
        before validation.

        Args:
            v (str): The value of the category field.

        Returns:
            str: The validated and normalized category value.

        Raises:
            ValueError: If the category is invalid.
        """
        if v:
            allowed = {"food", "electronic", "book"}
            if v.lower() not in allowed:
                raise ValueError(f"Invalid category: {v}. Must be one of {allowed}")
            return v.lower()
        return v
