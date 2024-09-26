import psycopg2
from psycopg2 import sql

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="business",  # Your database name
    user="postgres",    # Your PostgreSQL user
    password="thepassword",  # Your PostgreSQL password from Docker ENV
    host="localhost",   # Assuming PostgreSQL is running on localhost
    port="5432"         # Default PostgreSQL port
)

# Create a cursor object
cur = conn.cursor()

# List all tables in the public schema
cur.execute("""
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';
""")

# Fetch all table names
tables = cur.fetchall()

print("Tables in the database:")
for table in tables:
    print(table[0])

# Print contents of each table
for table in tables:
    print(f"\nContents of table {table[0]}:")
    cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table[0])))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Close the cursor and connection
cur.close()
conn.close()
