import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Product, Order, User

app = FastAPI(title="Mini Marketplace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductCreate(Product):
    pass

class OrderCreate(Order):
    pass

@app.get("/")
def read_root():
    return {"message": "Marketplace API running"}

@app.get("/schema")
def get_schema():
    return {
        "user": User.model_json_schema(),
        "product": Product.model_json_schema(),
        "order": Order.model_json_schema(),
    }

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Products
@app.post("/products")
def create_product(payload: ProductCreate):
    try:
        product_id = create_document("product", payload)
        return {"id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products")
def list_products(q: Optional[str] = None, category: Optional[str] = None, limit: int = 50):
    try:
        filter_dict = {}
        if q:
            filter_dict["title"] = {"$regex": q, "$options": "i"}
        if category and category != "all":
            filter_dict["category"] = category
        docs = get_documents("product", filter_dict, limit)
        for d in docs:
            d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}")
def get_product(product_id: str):
    try:
        from bson import ObjectId
        doc = db["product"].find_one({"_id": ObjectId(product_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Product not found")
        doc["id"] = str(doc.pop("_id"))
        return doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categories")
def list_categories():
    try:
        cats = db["product"].distinct("category") if db is not None else []
        cats = [c for c in cats if c]
        cats.sort()
        return cats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Orders
@app.post("/orders")
def create_order(payload: OrderCreate):
    try:
        order_id = create_document("order", payload)
        return {"id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/orders")
def list_orders(limit: int = 50):
    try:
        docs = get_documents("order", {}, limit)
        for d in docs:
            d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
