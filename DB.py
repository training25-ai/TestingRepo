class db():
  def __init__(self):
    self.database = ""
    self.host = ""
    self.user = ""
    self.password = ""
    self.port = 0
    self.sslmode = ""

  def set_connection_details(self,database,host,user,password,port,sslmode):
    if self.database == "" and self.host == "" and self.user == "" and self.password == "" and self.port == 0 and self.sslmode == "":
      self.database = database
      self.host = host
      self.user = user
      self.password = password
      self.port = port
      self.sslmode = sslmode
      print("Connection set")
    else:
      print("Connection already set")

  def get_connection_details(self):
    return self.database,self.host,self.user,self.port,self.sslmode

  def get_DB_connection(self):
    database,host,user,port,sslmode = self.get_connection_details()
    try:
      import psycopg2
    except Exception as e:
      print("psycopg2 not installed, try pip install psycopg2 and try again.")

    try:
      conn = psycopg2.connect(
          host=host,
          port=port,
          database=database,
          user=user,
          password=self.password,
          sslmode=sslmode
      )
      print("Database connection established successfully.")

      cursor = conn.cursor()
      return conn,cursor

    except Exception as e:
      print(f"Error connecting to the database: {e}")
      return None,None

  def get_db_version(self):
    conn,cursor = self.get_DB_connection()
    try:
      cursor.execute("SELECT version();")
      db_version = cursor.fetchone()
      print(f"Database Version: {db_version[0]}")
    except Exception as e:
        print(f"Error connecting to the database: {e}")
    finally:
      del cursor
      conn.close()

  def create_table(self,schema_name = "",table_name = "", primary_key_name = "",columns_datatype_dict = {}):
    conn,cursor = self.get_DB_connection()
    builded_query = f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} ({primary_key_name} SERIAL PRIMARY KEY,{', '.join([f'{key} {value}' for key, value in columns_datatype_dict.items()])});"
    try:
      cursor.execute(builded_query)
      conn.commit()
      print("Table created successfully.")
    except Exception as e:
        print(f"Error Creating table in the database: {e}")
    finally:
      del cursor
      conn.close()

  def insert_entry(self,schema_name = "",table_name = "", columns_value_dict = {}):
    conn,cursor = self.get_DB_connection()
    builded_query = f"""INSERT INTO {schema_name}.{table_name} ({', '.join(columns_value_dict.keys())}) VALUES ({', '.join([f"'{value}'" for value in columns_value_dict.values()])});"""
    try:
      cursor.execute(builded_query)
      conn.commit()
      print("Entry inserted successfully.")
    except Exception as e:
        print(f"Error inserting entry in the database: {e}")
    finally:
      del cursor
      conn.close()

  def delete_entry(self, schema_name = "", table_name = "", primary_key_name = "", primary_key_value = ""):
    conn,cursor = self.get_DB_connection()
    builded_query = f"""DELETE FROM {schema_name}.{table_name} WHERE {primary_key_name} = {primary_key_value};"""
    try:
      cursor.execute(builded_query)
      conn.commit()
      print("Entry deleted successfully.")
    except Exception as e:
        print(f"Error deleting entry in the database: {e}")
    finally:
      del cursor
      conn.close()

  def execute_query(self,query):
    conn,cursor = self.get_DB_connection()
    try:
      cursor.execute(query)
      conn.commit()
      print("Query executed successfully.")
    except Exception as e:
        print(f"Error executing query in the database: {e}")
    finally:
      del cursor
      conn.close()

  def fetch_data(self,query):
    conn,cursor = self.get_DB_connection()
    try:
      cursor.execute(query)
      data = cursor.fetchall()
      return data
    except Exception as e:
        print(f"Error executing query in the database: {e}")
    finally:
      del cursor
      conn.close()


