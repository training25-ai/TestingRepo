import psycopg2

def check_and_create_table():
    host = "ep-noisy-lake-a8k78ama-pooler.eastus2.azure.neon.tech"
    database = "playground"
    user = "shashank"
    password = "C0nsult@nt"
    schema = "ml"
    table_name = "shashank_table"

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=host, database=database, user=user, password=password, port=5432
        )
        cur = conn.cursor()

        # Check if table exists
        cur.execute(f"SELECT * FROM {schema}.{table_name} LIMIT 5;")
        print(f"✅ Table '{table_name}' exists.")
    
    except psycopg2.errors.UndefinedTable:
        print(f"⚠️ Table '{table_name}' does not exist. Creating it now...")

        # Create table if it does not exist
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {schema}.{table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            city VARCHAR(100)
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        print(f"✅ Table '{table_name}' created successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()
            print("🔄 Connection closed.")

# Run the function
check_and_create_table()
