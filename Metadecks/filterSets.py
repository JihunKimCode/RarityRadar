import csv

def filter_sets(file_path, target_sets, output_file="filtered_cards.csv"):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        fieldnames = reader[0].keys() if reader else []

        # Filter rows by target sets
        filtered_rows = [row for row in reader if row['Set'] in target_sets]

        # Write to one combined CSV file
        with open(output_file, "w", newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_rows)

        print(f"✅ Saved {len(filtered_rows)} filtered rows to {output_file}")

csv_file_path = "decklist.csv" 
target_sets = ["SSH", "RCL", "DAA", "VIV", "BST"]
filter_sets(csv_file_path, target_sets)
