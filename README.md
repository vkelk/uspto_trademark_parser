# uspto_trademark_parser
Simple scraper/parser that fetches XML data from https://bulkdata.uspto.gov/ then normalizes and inserts into database

## Usage

Install requirements `pip install -r requirements.txt`

Create database schema using `schema_create.sql`

Run parser `python tm_parser.py --parse`
