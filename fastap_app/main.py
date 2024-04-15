
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from psycopg_pool import AsyncConnectionPool


# Connect to an existing database
DATABASE_CONFIG = {
    "user": "summit_usr",
    "password": "P@ssw0rd202!",
    "host": "localhost",
    "port": "5432",
    "database": "redlen_pcct",
}

'''
def get_conn_str():
    return f"""
    dbname={os.getenv('POSTGRES_DB')}
    user={os.getenv('POSTGRES_USER')}
    password={os.getenv('POSTGRES_PASSWORD')}
    host={os.getenv('POSTGRES_HOST')}
    port={os.getenv('POSTGRES_PORT')}
    """
'''


def get_conn_str():
    return f"""
    dbname='redlen_pcct'
    user='summit_usr'
    password='P@ssw0rd202!'
    host='localhost'
    port='5432'
    """


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.async_pool = AsyncConnectionPool(conninfo=get_conn_str())
    yield
    await app.async_pool.close()


app = FastAPI(lifespan=lifespan)

# creating an endpoint/path


@app.get("/customers")
async def get_customers(request: Request):
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT * 
                FROM customers ORDER BY id ASC;
            """)
            results = await cur.fetchall()
            return {"customers": results}


@app.get("/customer")
async def get_customer(request: Request, customer_name):
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT * 
                FROM customers WHERE name = %s;
            """, (customer_name,))
            results = await cur.fetchall()
            return {"customer": results}


@app.get("/last_customer_id")
async def get_last_customer_id(request: Request):
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT * 
                FROM customers ORDER BY id DESC LIMIT 1;
            """)
            results = await cur.fetchall()
            return results[0][0]


@app.post("/customer")
async def insert_customer(request: Request, customer_name):
    try:
        async with request.app.async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                        INSERT INTO customers (name)
                        VALUES (%s) RETURNING *; 
                    """, (customer_name,))

                await conn.commit()

    except Exception:
        await conn.rollback()


@app.put("/customer")
async def update_customer(request: Request, customer_id, customer_name):
    """ update customer name based on the id """
    try:
        async with request.app.async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                        UPDATE customers SET name = %s
                        WHERE id = %s; 
                    """, (customer_name, customer_id))

                await conn.commit()

    except Exception:
        await conn.rollback()


@app.delete("/customer")
async def delete_customer(request: Request, customer_name):
    """ delete entry based on customer name """
    try:
        async with request.app.async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                        DELETE FROM customers WHERE name = %s;
                        """, (customer_name, ))
                rows_deleted = cur.rowcount
                await conn.commit()

    except Exception:
        await conn.rollback()
    finally:
        return rows_deleted
