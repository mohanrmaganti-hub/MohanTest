ServiceNow to SQL Server ETL

This project provides a simple, configurable ETL pipeline that extracts records from a ServiceNow instance and loads them into a SQL Server database.

Features
- Config-driven (config.yaml + .env)
- Modular: extract, transform, load
- Uses requests for ServiceNow REST API
- Uses pyodbc for SQL Server connectivity

Setup
1. Create a virtual environment and activate it:
   python3 -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Create a `.env` file from `.env.example` and fill in credentials.
4. Update `config.yaml` for table mappings and queries.

Run
   python -m etl.main

Notes
- This is a template and requires updating mappings and SQL statements to match your target schema.
