import kopf
import psycopg2
import os
from utils import _log_message

# Extract 'postgres' user credentials from environment variables
# Environment variables populated by secret defined in Deployment config
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']


# connect_pg
# description: Connect to input Postgres server, using secret credentials embedded in environment variables
# inputs: target_server (str)
# output: Connection
def connect_pg(target_server: str):
    try:
        conn = psycopg2.connect(
                host=target_server,
                database='postgres',
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                port=5432)
    except Exception as err:
        raise kopf.PermanentError(f"Connection creation failure! Error: {err}")
    return conn


# db_exists
# description: Check existence of target database on the target server
# inputs: target_server (str), target_database (str)
# output: bool
def db_exists(target_server: str, target_database: str) -> bool:
    db = None
    try:
        conn = connect_pg(target_server)
        cur = conn.cursor()
        conn.autocommit = True;
        cur.execute("""
            SELECT datname AS dbname 
            FROM pg_database
            WHERE datname = %s
        """, (target_database,))
        db = cur.fetchone()
        cur.close()
    except Exception as err:
        _log_message('error', f"Failed to validate database existence! Error: {err}")
    finally:
        if conn is not None:
            conn.close()
    if db is not None and target_database.lower() == db[0].lower():
        return True
    else:
        return False


# create_database
# description: Creates the target_database on the target_server
# inputs: target_server (str), target_database (str)
# output: None
def create_database(target_server: str, target_database: str):
    try:
        conn = connect_pg(target_server)
        cur = conn.cursor()
        # Create database cannot run in an explicit transaction scope, use autocommit
        conn.autocommit = True;
        cur.execute(f"CREATE DATABASE {target_database};")
        cur.close()
        if db_exists(target_server, target_database):
            _log_message('info', f"Database {target_database} created successfully")
        else:
            _log_message('warning', f"Failed to validate database creation for {target_database}")
    except Exception as err:
        _log_message('error', f"Error occurred during database creation for {target_database}! Error: {err}")
    finally:
        if conn is not None:
            conn.close()