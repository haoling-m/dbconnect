import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS PartialTestPlan;
        """,
        """
        CREATE TABLE PartialTestPlan (
            TestPlanID SERIAL PRIMARY KEY,
            TestPlanName VARCHAR(255),
            DetectorType VARCHAR(255),
            DetectorSN VARCHAR(255),
            TestSlot SMALLINT,
            VerIDTest BOOL,
            DieIDTest BOOL,
            LVDSCalTest BOOL,
            ThresholdTest BOOL,
            CalChainTest BOOL,
            Set18Test BOOL,
            TestPatternTest BOOL,
            PulserTest BOOL,
            CalibrationTest BOOL
        )
        """,
        """
        CREATE TABLE PartialCustomers (
            CustomerID SERIAL PRIMARY KEY,
            CustomerName VARCHAR(255)
        )
        """,
        """
        CREATE TABLE PartialTypes (
            PartialTypeID SERIAL PRIMARY KEY,
            PartialType VARCHAR(255)
        )
        """,
        """
        CREATE TABLE ResultPerAsic (
            AsicTestID SERIAL PRIMARY KEY,
            AsicIndex SMALLINT,
            Side SMALLINT,
            Die_ID BYTEA,
            Ver_ID SMALLINT,           
            TestPass BOOL,
            LvdsTestPass BOOL,
            CalibTestPass BOOL,
            Set18TestPass BOOL,
            ThresTestPass BOOL,            
            PatternTestPass BOOL,
            TemperatureTestPass BOOL,
            PulserTestPass BOOL,
            OddCounts INTEGER ARRAY,
            EvenCounts INTEGER ARRAY,
            Temperature_1 SMALLINT,
            Temperature_2 SMALLINT,
            NumNcp INTEGER
        )
        """,
        """ 
        CREATE TABLE ResultPartial ( 
            TestID SERIAL NOT NULL,          
            PartialSerialNumber VARCHAR(255),
            TestRunID INTEGER,
            AsicCount SMALLINT,
            PcbVersion SMALLINT,
            FpgaVersion SMALLINT,
            FpgaSubVersion SMALLINT,
            FpgaDate DATE,
            CustomerID INTEGER,
            PartialTypeID SMALLINT,
            TestPlanID SMALLINT,               
            TechnicianName VARCHAR(255),
            AsicSide_0 INTEGER,
            AsicSide_1 INTEGER,       
            TestPass BOOL,
            TestTime DATE,           
            PRIMARY KEY (PartialSerialNumber, TestRunID),
            FOREIGN KEY (CustomerID)
                REFERENCES PartialCustomers (CustomerID)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (PartialTypeID)
                REFERENCES PartialTypes (PartialTypeID)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (side_0_asic)
                REFERENCES asic_tests (asic_test_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (side_1_asic)
                REFERENCES asic_tests (asic_test_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (TestPlanID)
                REFERENCES PartialTestPlan (TestPlanID)
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
