import os
import json
import csv
from collections import defaultdict
from datetime import datetime

# Define folders you want to process
folder_list = [
    "../price-history-master/price-history-master/en/swsh1",
    "../price-history-master/price-history-master/en/swsh2",
    "../price-history-master/price-history-master/en/swsh3",
    "../price-history-master/price-history-master/en/swsh4",
    "../price-history-master/price-history-master/en/swsh5"
]

# Output CSV file
output_file = 'monthly_averages.csv'

# Open CSV for writing
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Set ID', 'Number', 'Grade', 'Month', 'Average'])

    # Loop through specified folders
    for setname in folder_list:
        print(f"🟢 Running {os.path.basename(setname)}...")
        if not os.path.isdir(setname):
            print(f"⚠️ Skipping {setname}: Not a folder")
            continue

        # Process each JSON file in the folder
        for filename in os.listdir(setname):
            if not filename.endswith('.tcgplayer.json'):
                continue

            card_number = filename.split('.')[0]
            filepath = os.path.join(setname, filename)

            try:
                with open(filepath, 'r') as f:
                    card_data = json.load(f)

                for grade, grade_data in card_data.get("data", {}).items():
                    monthly_data = defaultdict(list)

                    for date_str, entry in grade_data.get("history", {}).items():
                        month_str = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m")
                        monthly_data[month_str].append(entry["avg"])

                    for month, avg_list in monthly_data.items():
                        avg = sum(avg_list) / len(avg_list)
                        writer.writerow([os.path.basename(setname), card_number, grade, month, round(avg, 2)])

            except Exception as e:
                print(f"⚠️ Skipped {filepath}: {e}")

print(f"✅ All data saved to {output_file}")
