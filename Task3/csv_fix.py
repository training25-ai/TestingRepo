import csv

csv_path = "/Users/sunda/Downloads/Task3_dB_dataUpload/shashank_data.csv"
fixed_csv_path = "/Users/sunda/Downloads/Task3_dB_dataUpload/shashank_data_fixed.csv"

with open(csv_path, "r", newline="", encoding="utf-8") as infile, \
     open(fixed_csv_path, "w", newline="", encoding="utf-8") as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        cleaned_row = [cell.strip('"') for cell in row]  # Remove double quotes
        writer.writerow(cleaned_row)

print(f"✅ Fixed CSV saved as: {fixed_csv_path}")
