import requests
import sys
import os
import psycopg2
from dotenv import load_dotenv
from requests import JSONDecodeError, ConnectionError, ConnectTimeout
from typing import Optional, List

# Calculate the path to the root directory (one level up from the script directory)
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)
from config.config import DAY
from src.utils import OFFERS_START_DATE, OFFERS_END_DATE
from src.utils import *


# Load env file
load_dotenv()
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
DB_USER = os.getenv("DB_USER")
X_RAPIDAPI_KEY = os.getenv("X_RAPIDAPI_KEY")
X_RAPIDAPI_HOST = os.getenv("X_RAPIDAPI_HOST")

def run_query(sql_query, params=None):
    """Run a SQL query and return the result. Parameters are passed separately to avoid SQL injection."""
    try:
        conn = psycopg2.connect(dbname='offers', user=DB_USER, host='localhost', port='5432')
        cur = conn.cursor()
        
        # Execute the query with parameters safely
        cur.execute(sql_query, params or ())
        
        # For SELECT queries
        if sql_query.strip().upper().startswith("SELECT"):
            result = cur.fetchall()
        else:  # For INSERT/UPDATE/DELETE queries
            conn.commit()
            result = None
        
        cur.close()
        conn.close()
        
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def fruit_and_veg_offers(date: str):
    """Get the fruit and veg offers from the database for a given week."""
    # Calculate the start and end of the week for the given date
    start_of_week = get_week_start_date(date)
    
    
    # Parameterized SQL query
    sql = "SELECT * FROM offers_veg WHERE offer_from = %s;"
    return run_query(sql, (start_of_week,))

def wine_selection_or_offers(wine_type: str = None, date: str = None):
    """Get the wine selection for either red, rose, white wines or all wines from the database. Filter for offers on a specific date."""
    where_clauses = []
    params = []
    
    if date:
        select_clause = "SELECT id, product_name, price_offer, price_regular, wine_type, grape_variety"
        start_of_week = get_week_start_date(date)
        where_clauses.append("offer_from = %s")
        params.append(start_of_week)
    else:
        select_clause = "SELECT id, product_name, price_regular, wine_type, grape_variety"
    
    if wine_type:
        where_clauses.append("wine_type = %s")
        params.append(wine_type)
    
    where_clause = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    sql = f"{select_clause} FROM offers_wine{where_clause};"
    
    return run_query(sql, params)



def fridge_items(date: str):
    """Get the items in the fridge for a given date."""
    sql = "SELECT vegetables FROM fridge WHERE date = %s;"
    return run_query(sql, (date,))
