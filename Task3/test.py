import pandas as pd

csv_path = "/Users/sunda/Downloads/Task3_dB_dataUpload/shashank_data.csv"

df = pd.read_csv(csv_path)
print("CSV Columns:", df.columns.tolist())
