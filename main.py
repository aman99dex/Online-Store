from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database_models import Product
from database import session, engine
import database_models
from schemas import ProductCreate, ProductUpdate, ProductResponse
from typing import List

database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
@app.get("/")
def greetuser():
    return "welcome to my store"

products = [
    Product(id=1, name="Laptop", description="High-performance laptop", price=999.99, quantity=10),
    Product(id=2, name="Mouse", description="Wireless mouse", price=29.99, quantity=50),
    Product(id=3, name="Keyboard", description="Mechanical keyboard", price=79.99, quantity=30)
]
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()

@app.get("/products/", response_model=List[ProductResponse])
def get_all_products(db = Depends(get_db)):
    products = db.query(database_models.Product).all()
    return products

@app.get("/products/{id}", response_model=ProductResponse)
def get_product_by_id(id: int, db = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db = Depends(get_db)):
    db_product = database_models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{id}", response_model=ProductResponse)
def update_product(id: int, product: ProductUpdate, db = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{id}")
def delete_product(id: int, db = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
