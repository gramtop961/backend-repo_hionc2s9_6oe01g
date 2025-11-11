"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: Optional[str] = Field(None, description="Address")
    phone: Optional[str] = Field(None, description="Phone number")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    image_url: Optional[str] = Field(None, description="Primary image URL")
    rating: float = Field(4.5, ge=0, le=5, description="Average rating")
    stock: int = Field(100, ge=0, description="Units in stock")
    in_stock: bool = Field(True, description="Whether product is in stock")

class OrderItem(BaseModel):
    product_id: str = Field(..., description="ID of the product")
    title: str = Field(..., description="Product title snapshot at order time")
    price: float = Field(..., ge=0, description="Unit price at order time")
    quantity: int = Field(..., ge=1, description="Quantity ordered")
    image_url: Optional[str] = None

class Order(BaseModel):
    """
    Orders collection schema
    Collection name: "order"
    """
    buyer_name: str = Field(..., description="Buyer full name")
    buyer_email: EmailStr = Field(..., description="Buyer email")
    buyer_address: str = Field(..., description="Shipping address")
    buyer_phone: Optional[str] = Field(None, description="Phone number")
    items: List[OrderItem] = Field(..., description="List of items in the order")
    subtotal: float = Field(..., ge=0)
    shipping: float = Field(0, ge=0)
    total: float = Field(..., ge=0)
    status: str = Field("pending", description="Order status")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
