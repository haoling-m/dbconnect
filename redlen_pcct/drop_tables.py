import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS partial_test_plans CASCADE;
        """,
        """
        DROP TABLE IF EXISTS partial_customers CASCADE;
        """,
        """
        DROP TABLE IF EXISTS partial_types CASCADE;
        """,
        """
        DROP TABLE IF EXISTS asic_tests CASCADE;
        """,
        """ 
        DROP TABLE IF EXISTS partial_build_tests CASCADE;
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