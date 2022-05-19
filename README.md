https://www.postgresqltutorial.com/postgresql-python/

This PostgreSQL Python section shows you how to work with the PostgreSQL database using the Python programming language.

Python has various database drivers for PostgreSQL. Currently, the psycopg is the most popular PostgreSQL database adapter for the Python language. The psycopg fully implements the Python DB-API 2.0 specification.

The current version of the psycopg is 2 or psycopg2. The psycopg2 database adapter implemented in C as a libpq wrapper resulting in both fast and secure. The psycopg2 provides many useful features such as client-side and server-side cursors, asynchronous notification and communication, COPY command support, etc.

Besides, the psycopg2 driver supports many Python types out-of-the-box. The psycopg2 matches Python objects to the PostgreSQL data types, e.g., list to the array, tuples to records, and dictionary to hstore.  If you want to customize and extend the type adaption, you can use a flexible object adaption system.

This PostgreSQL Python section covers the most common activities for interacting with PostgreSQL in Python application:

Connecting to the PostgreSQL database server – show you how to connect to the PostgreSQL database server from Python.
Creating new PostgreSQL tables in Python – show you how to create new tables in PostgreSQL from Python.
Inserting data into the PostgreSQL table in Python – explain to you how to insert data into a PostgreSQL database table in Python.
Updating data in the PostgreSQL table in Python – learn various ways to update data in the PostgreSQL table.
Transaction – show you how to perform transactions in Python.
Querying data from the PostgreSQL tables – walk you through the steps of querying data from the PostgreSQL tables in a Python application.
Calling a PostgreSQL function in Python – show you step by step how to call a PostgreSQL function in Python.
Calling a PostgreSQL stored procedure in Python – guide you on how to call a stored procedure from in a Python application.
Handling PostgreSQL BLOB data in Python– give you an example of inserting and selecting the PostgreSQL BLOB data in a Python application.
Deleting data from PostgreSQL tables in Python – show you how to delete data in a table in Python.
For demonstration purposes, we will use the suppliers sample database. The following picture illustrates the structure of the suppliers database:

PostgreSQL Python Sample Database Diagram
The suppliers database has the following tables:

 vendors table: stores vendor data.
 parts table: stores parts data.
 parts_drawings table: stores the drawing of a part.
 vendor_parts table: stores the data of which parts supplied by which vendor.