from fastapi import FastAPI
from models import Product


app = FastAPI()
@app.get("/")
def greetuser():
    return "welcome to my store"

products = [
    Product(id=1, name="Laptop", description="High-performance laptop", price=999.99, quantity=10),
    Product(id=2, name="Mouse", description="Wireless mouse", price=29.99, quantity=50),
    Product(id=3, name="Keyboard", description="Mechanical keyboard", price=79.99, quantity=30)
]

@app.get("/products")
def get_all_products():
    return products

@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    return {"error": "Product not found"}

@app.post("/product")
def create_product(product: Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product updated successfully"
    return {"error": "Product not found"}

@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            products.pop(i)
            return "Product deleted successfully"
    return {"error": "Product not found"}
