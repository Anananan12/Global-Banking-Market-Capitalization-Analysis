import requests
from bs4 import BeautifulSoup
import pandas as pd 
import sqlite3
import numpy as np 
from datetime import datetime

url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
db_name = 'Banks.db'
table_name = 'Largest_banks'
csv_path = './Largest_banks_data.csv'
csv_transform = './Neo_Largest_bank_data.csv'
Table_Attributes_upon_Extraction_only = ['Name', 'MC_USD_Billion']
log_file = "log_file.txt" 

def log_progress(message):
    timestamp_format = '%Y-%m-%d %H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file, "a") as f: 
        f.write(timestamp + ',' + message + '\n') 

def extract(url, table_attribs):
    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')

    tables = data.find_all('tbody')
    table = tables[0]

    headers = []
    for header in table.find_all('th')[1:]:
        headers.append(header.text.strip())

    # Extract rows
    rows = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')[1:]
        cells = [cell.text.strip() for cell in cells]
        if cells:
            rows.append(cells)
    
    column_names = table_attribs
    df = pd.DataFrame(rows, columns=column_names)
    print("DataFrame before conversion:")
    print(df)

    return df

def transform(df, csv_path):
    df['MC_USD_Billion'] = pd.to_numeric(df['MC_USD_Billion'], errors='coerce')
    
    # Check if there are any non-numeric values
    print(df['MC_USD_Billion'].head())

    # Apply the conversion and rounding
    df['MC_GBP_Billion'] = np.round(df['MC_USD_Billion'] * 0.8, 2)
    df['MC_EUR_Billion'] = np.round(df['MC_USD_Billion'] * 0.93, 2)
    df['MC_INR_Billion'] = np.round(df['MC_USD_Billion'] * 82.95, 2)

    return df

def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    try:
        cursor = sql_connection.cursor()
        cursor.execute(query_statement)
        results = cursor.fetchall()
        
        # Get column names from cursor description
        column_names = [description[0] for description in cursor.description]
        
        # Create a DataFrame for better readability (optional)
        df = pd.DataFrame(results, columns=column_names)
        
        # Print the query and its results
        print(f"Query:\n{query_statement}\n")
        print(f"Output:\n{df}\n")
        
    except Exception as e:
        print(f"An error occurred: {e}")

log_progress('Preliminaries complete. Initiating ETL process')

log_progress('Data extraction complete. Initiating Transformation process')
extracted_data = extract(url, Table_Attributes_upon_Extraction_only)

log_progress('Data transformation complete. Initiating Loading process')
transformed_data = transform(extracted_data, csv_path)

log_progress('Data saved to CSV file')
load_to_csv(transformed_data, csv_transform)

conn = sqlite3.connect(db_name)
log_progress('SQL Connection initiated')

log_progress('Data loaded to Database as a table, Executing queries')
load_to_db(transformed_data, conn, table_name)

# Verify if the table exists
query_check_table = "SELECT name FROM sqlite_master WHERE type='table' AND name='Largest_banks';"
run_query(query_check_table, conn)

query1 = "SELECT * FROM Largest_banks"
run_query(query1, conn)

query2 = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
run_query(query2, conn)

query3 = "SELECT Name from Largest_banks LIMIT 5"
run_query(query3, conn)

log_progress('Process Complete')

conn.close()
log_progress('Server Connection closed')
