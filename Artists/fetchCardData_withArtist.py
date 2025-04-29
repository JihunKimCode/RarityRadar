import os
import json
import requests
import pandas as pd
from collections import defaultdict
from datetime import datetime

# Step 1: Fetch Pokémon Card Info
def fetch_pokemon_cards(set_ids):
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
            "Artist": card.get("artist", "Unknown"),
            "Rarity": card.get("rarity", "Unknown"),
        } for card in all_cards
    ]

    return pd.DataFrame(card_list)

# Step 2: Compute Monthly Averages
def process_price_history(folder_list):
    records = []

    for set_folder in folder_list:
        print(f"🟢 Processing {os.path.basename(set_folder)}...")
        if not os.path.isdir(set_folder):
            print(f"⚠️ Skipping {set_folder}: Not a folder")
            continue

        for filename in os.listdir(set_folder):
            if not filename.endswith('.tcgplayer.json'):
                continue

            card_number = filename.split('.')[0]
            filepath = os.path.join(set_folder, filename)

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
                        records.append([
                            os.path.basename(set_folder),
                            card_number,
                            grade,
                            month,
                            round(avg, 2)
                        ])

            except Exception as e:
                print(f"⚠️ Skipped {filepath}: {e}")

    return pd.DataFrame(records, columns=["Set ID", "Number", "Grade", "Month", "Average"])

# Step 3: Merge and Output Final CSV
def merge_and_save(card_df, price_df, output_file="merged_pokemon_data_with_artist.csv"):
    merged_df = price_df.merge(card_df, on=["Set ID", "Number"], how="left")
    merged_df = merged_df[["Set ID", "Number", "Name", "Artist", "Rarity", "Grade", "Month", "Average"]]
    merged_df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"✅ Merged data saved to {output_file}")

# Main
if __name__ == "__main__":
    set_ids = ["swsh1", "swsh2", "swsh3", "swsh4", "swsh5"]
    folders = [f"../price-history-master/price-history-master/en/{sid}" for sid in set_ids]

    card_df = fetch_pokemon_cards(set_ids)
    price_df = process_price_history(folders)
    merge_and_save(card_df, price_df)
