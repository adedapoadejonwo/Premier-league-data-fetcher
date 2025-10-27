import os
import psycopg
from dotenv import load_dotenv
import logging

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def get_conn():
    """Get database connection with error handling"""
    if not DB_URL:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    try:
        return psycopg.connect(DB_URL)
    except psycopg.Error as e:
        logging.error(f"Database connection failed: {e}")
        raise
