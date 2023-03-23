import kopf
import psycopg2
import os
from utils import _log_message

#extract postgres credentials from environment variables
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

def connect_pg(server: str):
    try:
        conn = psycopg2.connect(
                host=server,
                database='postgres',
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                port=5432)
    except Exception as err:
        _log_message('error', f"Error: {err}")
        raise kopf.PermanentError(f"Error:{err}")
    return conn

def db_exists(target_server: str, target_database: str) -> bool:
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
        if db is not None:
            if target_database.lower() == db[0].lower():
                returnval = True
        else:
            returnval = False
    except Exception as err:
        _log_message('error', f"Error: {err}")
    finally:
        if conn is not None:
            conn.close()
    return returnval

def create_database(target_server: str, target_database: str):
    try:
        conn = connect_pg(target_server)
        cur = conn.cursor()
        #create database cannot run in an explicit transaction scope
        conn.autocommit = True;
        cur.execute(f"CREATE DATABASE {target_database};")
        cur.close()
        if db_exists(target_server, target_database):
            _log_message('info', f"{target_database} created successfully")
        else:
            _log_message('info', f"failed to create {target_database}")
    except Exception as err:
        _log_message('error', f"Error: {err}")
    finally:
        if conn is not None:
            conn.close()