from typing import Any, List, Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    details: Optional[Any] = None


class ProductResponse(BaseModel):
    id: int
    product_name: str
    category: str
    quantity: int
    price: float

    model_config = {"from_attributes": True}


class FoodProductResponse(ProductResponse):
    mfg_date: str
    expiry_date: str


class ElectronicProductResponse(ProductResponse):
    purchase_date: str
    warranty_period: int


class BookProductResponse(ProductResponse):
    author: str
    publication_year: int


class ProductListResponse(BaseModel):
    products: List[ProductResponse]

    model_config = {"from_attributes": True}


class ProductCreateResponse(BaseModel):
    message: str
    product: ProductResponse

    model_config = {"from_attributes": True}


class ProductUpdateResponse(BaseModel):
    message: str
    product: ProductResponse

    model_config = {"from_attributes": True}


class ProductDeleteResponse(BaseModel):
    message: str
