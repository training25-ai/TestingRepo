import psycopg2
import pandas as pd
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Database connection details
DB_CONFIG = {
    "host": "ep-noisy-lake-a8k78ama-pooler.eastus2.azure.neon.tech",
    "database": "playground",
    "user": "shashank",
    "password": "C0nsult@nt",
    "schema": "ml",
    "table": "shashank_table"
}

# CSV File Path
CSV_FILE = "/Users/sunda/Downloads/Task3/TestingRepo/Task3/shashank_data.csv"

def connect_db():
    """Establish database connection."""
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=5432
    )

def import_csv_to_db():
    """Reads CSV and inserts new data into PostgreSQL table."""
    try:
        conn = connect_db()
        cur = conn.cursor()

        # Read CSV file
        df = pd.read_csv(CSV_FILE)

        # Ensure column names match database table
        if list(df.columns) != ["name", "age", "city"]:
            print("⚠️ CSV column mismatch! Ensure CSV has: name, age, city")
            return
        
        # Insert new records
        for _, row in df.iterrows():
            cur.execute(
                f"""
                INSERT INTO {DB_CONFIG['schema']}.{DB_CONFIG['table']} (name, age, city)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                """,
                (row["name"], row["age"], row["city"])
            )

        conn.commit()
        print("✅ New data imported successfully!")

    except Exception as e:
        print(f"❌ Error importing data: {e}")
    
    finally:
        cur.close()
        conn.close()

class CSVWatcher(FileSystemEventHandler):
    """Watches for CSV file changes."""
    
    def on_modified(self, event):
        if event.src_path == CSV_FILE:
            print("🔄 CSV file updated. Importing new data...")
            import_csv_to_db()

def start_monitoring():
    """Starts watching the CSV file for changes."""
    observer = Observer()
    event_handler = CSVWatcher()
    observer.schedule(event_handler, os.path.dirname(CSV_FILE), recursive=False)
    observer.start()

    print(f"👀 Watching for changes in {CSV_FILE}...")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Initial import
    import_csv_to_db()
    
    # Start watching for updates
    start_monitoring()
