import requests
import pandas as pd

def fetch_pokemon_cards():
    set_ids = ["swsh1","swsh2","swsh3","swsh4","swsh5"]  # Add more set IDs as needed
    all_cards = []
    
    for set_id in set_ids:
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
                print(f"Failed to fetch data: {e}")
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
    df.to_excel("pokemon_cards.xlsx", index=False)
    print("Excel file 'pokemon_cards.xlsx' created successfully.")

if __name__ == "__main__":
    fetch_pokemon_cards()
