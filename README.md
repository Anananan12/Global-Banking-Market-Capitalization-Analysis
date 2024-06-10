# Global-Banking-Market-Capitalization-Analysis
## Project Overview
This project involves compiling and transforming data on the top 10 largest banks in the world by market capitalization. The goal is to present the market capitalization in multiple currencies (USD, GBP, EUR, and INR) to cater to an international management team. The data will be stored both as a CSV file and a database table for easy querying.

### Project Components
#### 1. Data Collection
Extract the list of the top 10 largest banks by market capitalization from the provided URL.
#### 2. Data Transformation

Convert the market capitalization values from USD to GBP, EUR, and INR using the exchange rates from a provided CSV file.
#### 3. Data Storage

Save the transformed data into a CSV file.
Store the data in a database table for easy access by managers.
#### 4. Database Queries

Run specific queries to extract information for different office locations.

### Project Structure
'Banks_db': Database file (SQLite/MySQL/PostgreSQL) with a table for the processed data.


'banks_project.py': Python script to process the data.


'exchange_rate.csv': Contains the exchange rates for USD, GBP, EUR, and INR.

'Neo_Largest_bank_data.csv': banks data after transformation.

'log_file.txt': code running process log.

### Prerequisites
Python 3.x

Pandas library

SQLAlchemy library

BeautifulSoup library (for web scraping)

SQLite/MySQL/PostgreSQL database

### Instructions
#### 1. Clone the Repository
git clone <repository_url>
cd <repository_directory>
#### 2. Install Dependencies
pip install pandas sqlalchemy beautifulsoup4
#### 3. Data Processing
python scripts/data_processing.py

### Logging
The script maintains a log of its operations, including data extraction, transformation, and loading processes. Logs are stored in logs/project.log.

### Author
Xuhui An

### License
This project is licensed under the MIT License.

### Contact
For any issues or questions, please contact xuhui.an12@gmail.com.
