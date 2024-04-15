from fastapi import FastAPI, HTTPException
import psycopg2
from fastapi import Depends

app = FastAPI()

# Replace the placeholder values with your PostgreSQL credentials
"""DATABASE_CONFIG = {
    "user": "your_username",
    "password": "your_password",
    "host": "your_host",
    "port": "your_port",  # Default is 5432
    "database": "your_database",
}
"""
DATABASE_CONFIG = {
    "user": "summit_usr",
    "password": "P@ssw0rd202!",
    "host": "localhost",
    "port": "5432",
    "database": "redlen_pcct",
}


def get_connection():
    return psycopg2.connect(**DATABASE_CONFIG)


@app.on_event("startup")
async def startup_event():
    app.db_connection = get_connection()


@app.on_event("shutdown")
async def shutdown_event():
    app.db_connection.close()

# 3.Create CRUD operations using psycopg2:


def get_db():
    db = app.db_connection
    cursor = db.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


# Create operation
@app.post("/items/")
async def create_item(name: str, db: Depends(get_db)):
    query = "INSERT INTO items (name) VALUES (%s) RETURNING id, name;"
    db.execute(query, (name,))
    result = db.fetchone()
    app.db_connection.commit()
    return {"id": result[0], "name": result[1]}


# Read operation
@app.get("/items/{item_id}")
async def read_item(item_id: int, db: Depends(get_db)):
    query = "SELECT id, name FROM items WHERE id = %s;"
    db.execute(query, (item_id,))
    result = db.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": result[0], "name": result[1]}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
