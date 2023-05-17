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
            test_plan_name VARCHAR(255) NOT NULL,
            detector_type VARCHAR(255) NOT NULL,
            detector_sn VARCHAR(255) NOT NULL,
            test_slot INTEGER NOT NULL,
            ver_id_test BOOL NOT NULL,
            die_id_test BOOL NOT NULL,
            threshold_file_test BOOL NOT NULL,
            chain_file_test BOOL NOT NULL,
            set18_file_test BOOL NOT NULL,
            test_pattern_verification BOOL NOT NULL,
            pulser_statistics_test BOOL NOT NULL,
            calibration_test BOOL NOT NULL
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
            partial_type VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE asic_tests (
            asic_test_id SERIAL PRIMARY KEY,
            die_id VARCHAR(255) NOT NULL,
            side INTEGER NOT NULL,
            test_run INTEGER NOT NULL,
            pass BOOL NOT NULL,
            threshold_file_test BOOL NOT NULL,
            chain_file_test BOOL NOT NULL,
            set18_file_test BOOL NOT NULL,
            test_pattern_verification BOOL NOT NULL,
            pulser_statistics_test BOOL NOT NULL,
            pulser_ncp VARCHAR(255) NOT NULL,
            num_ncp INTEGER NOT NULL, 
            cc1_even TEXT NOT NULL,
            cc1_odd TEXT NOT NULL
        )
        """,
        """ 
        CREATE TABLE partial_build_tests ( 
            test_id SERIAL NOT NULL,          
            partial_sn VARCHAR(255) NOT NULL,
            test_run_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            partial_type_id INTEGER NOT NULL,
            test_plan_id INTEGER NOT NULL,
            detector_ver_build VARCHAR(255) NOT NULL,
            technician_name VARCHAR(255),
            test_date VARCHAR(255),
            partial_test_pass BOOL NOT NULL,
            side_0_asic INTEGER NOT NULL,
            side_1_asic INTEGER NOT NULL,
            PRIMARY KEY (partial_sn, test_run_id),
            FOREIGN KEY (customer_id)
                REFERENCES partial_customers (customer_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (partial_type_id)
                REFERENCES partial_types (partial_type_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (side_0_asic)
                REFERENCES asic_tests (asic_test_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (side_1_asic)
                REFERENCES asic_tests (asic_test_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (test_plan_id)
                REFERENCES partial_test_plans (test_plan_id)
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
