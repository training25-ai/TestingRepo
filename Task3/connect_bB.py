import os
import psycopg2

def truncate_table(conn, table_name, schema):
    try:
        with conn.cursor() as cur:
            cur.execute(f'TRUNCATE TABLE {schema}.{table_name} RESTART IDENTITY CASCADE;')
            print(f"Table '{table_name}' has been truncated and is now empty.")
    except Exception as e:
        print(f"Error truncating table: {e}")

def main():
    host = "ep-noisy-lake-a8k78ama-pooler.eastus2.azure.neon.tech"
    database = "playground"
    port = 5432
    user = os.getenv("DB_USER", "shashank")  
    password = os.getenv("DB_PASSWORD", "C0nsult@nt")
    schema = "ml"
    table_name = "shashank_table"

    try:
        conn = psycopg2.connect(
            host=host, database=database, user=user, password=password, port=port
        )
        conn.autocommit = True

        truncate_table(conn, table_name, schema)

    except Exception as e:
        print(f"Database connection error: {e}")
    
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()
