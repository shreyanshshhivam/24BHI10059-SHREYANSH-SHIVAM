from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import pymongo
from datetime import datetime

app = FastAPI()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["inventory_db"]
products_collection = db["products"]

products_collection.create_index("sku", unique=True)

class Product(BaseModel):
    sku: str = Field(..., min_length=3)
    name: str = Field(..., min_length=2)
    category: str
    price: float = Field(..., gt=0)
    quantity: int = Field(default=0, ge=0)

class StockUpdate(BaseModel):
    quantity_change: int

@app.post("/products/", status_code=status.HTTP_201_CREATED)
def add_product(product: Product):
    product_dict = product.model_dump()
    product_dict["last_updated"] = datetime.now()
    
    try:
        products_collection.insert_one(product_dict)
        product_dict["_id"] = str(product_dict["_id"])
        return {"message": "Product added successfully", "product": product_dict}
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=400, detail=f"Product with SKU '{product.sku}' already exists.")

@app.get("/products/")
def view_all_products():
    products = list(products_collection.find())
    for p in products:
        p["_id"] = str(p["_id"])
    return {"total_items": len(products), "inventory": products}

@app.get("/products/{sku}")
def get_product(sku: str):
    product = products_collection.find_one({"sku": sku})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product["_id"] = str(product["_id"])
    return product

@app.patch("/products/{sku}/stock")
def update_stock(sku: str, update: StockUpdate):
    product = products_collection.find_one({"sku": sku})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_quantity = product["quantity"] + update.quantity_change
    
    if new_quantity < 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot remove {abs(update.quantity_change)} items. Only {product['quantity']} in stock."
        )

    products_collection.update_one(
        {"sku": sku},
        {"$set": {"quantity": new_quantity, "last_updated": datetime.now()}}
    )
    
    return {"message": "Stock updated", "sku": sku, "new_quantity": new_quantity}

@app.delete("/products/{sku}")
def delete_product(sku: str):
    result = products_collection.delete_one({"sku": sku})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": f"Product '{sku}' deleted successfully."}