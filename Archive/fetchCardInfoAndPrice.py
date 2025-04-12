import os
import json
import csv
import requests
import pandas as pd
from collections import defaultdict
from datetime import datetime

# === Step 1: Fetch Pokémon Card Info from API ===
def fetch_pokemon_cards(set_ids, output_file="pokemon_cards.csv"):
    all_cards = []
    for set_id in set_ids:
        print(f"🟢 Fetching {set_id}...")
        current_page = 1
        has_more_data = True
        url = f"https://api.pokemontcg.io/v2/cards?q=set.id:{set_id}"

        while has_more_data:
            try:
                response = requests.get(f"{url}&page={current_page}")
                if response.status_code != 200:
                    raise Exception(f"Network response was not ok: {response.status_code}")

                data = response.json()
                cards = data.get("data", [])
                all_cards.extend(cards)

                if len(cards) < 250:
                    has_more_data = False
                else:
                    current_page += 1
            except Exception as e:
                print(f"⚠️ Failed to fetch data: {e}")
                has_more_data = False

    card_list = [
        {
            "Set ID": card.get("set", {}).get("id", "N/A"),
            "Number": card.get("number", "N/A"),
            "Name": card.get("name", "N/A"),
            "Rarity": card.get("rarity", "Unknown")
        } for card in all_cards
    ]

    df = pd.DataFrame(card_list)
    df.to_csv(output_file, index=False)
    print(f"✅ Card data saved to {output_file}")
    return output_file

# === Step 2: Extract Monthly Average Prices from JSON Files ===
def process_price_history(folder_list, output_file="monthly_averages.csv"):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Set ID', 'Number', 'Grade', 'Month', 'Average'])

        for setname in folder_list:
            print(f"🟢 Running {os.path.basename(setname)}...")
            if not os.path.isdir(setname):
                print(f"⚠️ Skipping {setname}: Not a folder")
                continue

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

    print(f"✅ Price history saved to {output_file}")
    return output_file

# === Step 3: Merge Card Info with Price Averages ===
def merge_csv_data(cards_csv, averages_csv, output_file="merged_pokemon_data.csv"):
    cards_df = pd.read_csv(cards_csv, encoding="ISO-8859-1")
    averages_df = pd.read_csv(averages_csv, encoding="ISO-8859-1")

    cards_df.columns = cards_df.columns.str.strip()
    averages_df.columns = averages_df.columns.str.strip()

    if cards_df.shape[1] == 1:
        cards_df = cards_df[cards_df.columns[0]].str.split(r'\0t|\,', expand=True)
        cards_df.columns = ["Set ID", "Number", "Name", "Rarity"]

    if averages_df.shape[1] == 1:
        averages_df = averages_df[averages_df.columns[0]].str.split(r'\t|,', expand=True)
        averages_df.columns = ["Set ID", "Number", "Grade", "Month", "Average"]

    merged_df = averages_df.merge(cards_df, on=["Set ID", "Number"], how="left")
    merged_df = merged_df[["Set ID", "Number", "Name", "Rarity", "Grade", "Month", "Average"]]
    merged_df.to_csv(output_file, index=False, sep=",", encoding="utf-8")

    print(f"✅ Merged data saved to {output_file}")


# === Run All Steps Together ===
if __name__ == "__main__":
    set_ids = ["swsh1", "swsh2", "swsh3", "swsh4", "swsh5"]
    folders = [f"../price-history-master/price-history-master/en/{sid}" for sid in set_ids]

    cards_csv = fetch_pokemon_cards(set_ids)
    prices_csv = process_price_history(folders)
    merge_csv_data(cards_csv, prices_csv)
