import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS partial_test_plans;
        """,
        """
        CREATE TABLE partial_test_plans (
            test_plan_id SERIAL PRIMARY KEY,
            customer_name VARCHAR(255) NOT NULL,
            partial_type VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE partial_customers (
            customer_id SERIAL PRIMARY KEY,
            customer_name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE partial_types (
            partial_type_id SERIAL PRIMARY KEY,
            customer_name VARCHAR(255) NOT NULL
        )
        """,
        """ 
        CREATE TABLE partial_builders (
            partial_sn VARCHAR(255) PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            FOREIGN KEY (customer_id)
                REFERENCES partial_customers (customer_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
