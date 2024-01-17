import csv
import psycopg2
import yaml

# Load the Docker Compose YAML file
with open('docker-compose.yml', 'r') as f:
    compose_config = yaml.safe_load(f)

# Extract the PostgreSQL configuration from the Docker Compose file
pg_config = compose_config['services']['db']

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname='postgres',
    user='postgres',
    password='postgres'
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Create the table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS EmployeeData (
        ID Int PRIMARY KEY,
        First_Name VARCHAR,
        Last_Name VARCHAR,
        Email VARCHAR,
        Gender VARCHAR,
        Ip_Address VARCHAR
    )
''')


# Read the data from the CSV file and insert it into the database

with open('SRDataEngineerChallenge_DATASET.csv', 'r') as f:

    header = f.readline().strip().split(',')

    # Capitalize the header names
    capitalized_header = [column.capitalize() for column in header]

    reader = csv.DictReader(f, fieldnames=capitalized_header)
    for row in reader:
        # Perform transformations on columns if needed
        transformed_row = {
            'Id': row['Id'],
            'First_Name': row['First_name'].upper(),
            'Last_Name': row['Last_name'].upper(),
            'Email': row['Email'].lower(),
            'Gender': row['Gender'],
            'Ip_address': row['Ip_address']
        }
        
        # Insert the transformed row into the database
        cur.execute('''
            INSERT INTO EmployeeData (ID, First_Name, Last_Name, Email, Gender, Ip_address)
            VALUES (%(Id)s, %(First_Name)s, %(Last_Name)s, %(Email)s, %(Gender)s, %(Ip_address)s)
        ''', transformed_row)

       
# Commit the changes and close the database connection
conn.commit()
cur.close()
conn.close()
