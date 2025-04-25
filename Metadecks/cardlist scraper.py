import requests
from bs4 import BeautifulSoup
import csv

# Step 1: Scrape Decks name and href
def parse_deck_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    decks = []

    # Extract deck name and index
    for row in soup.select('.data-table.striped tr')[1:]:
        deck_name = row.select_one('td a').text.strip() if row.select_one('td a') else ''
        deck_url = row.select_one('td a')['href'] if row.select_one('td a') else ''
        deck_index = deck_url.split('/')[-1] if deck_url else ''
        
        decks.append({'name': deck_name, 'index': deck_index})

    return decks

# Step 2: Scrape card list from each decks
def parse_decklist_cards(url, deck_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = []

    # Select all cards inside the decklist
    for card in soup.select('[data-text-decklist] .decklist-card'):
        count = float(card.select_one('.card-count').text.strip() if card.select_one('.card-count') else 0)
        name = card.select_one('.card-name').text.strip() if card.select_one('.card-name') else ''
        set = card.get('data-set', '')
        price_text = card.select_one('.card-price.usd').text.strip() if card.select_one('.card-price.usd') else '$0.00'
        price = float(price_text.replace('$', '')) if price_text else 0
        card_url = card.select_one('.card-price.usd')['href'] if card.select_one('.card-price.usd') else ''

        cards.append({'deck_name': deck_name, 'name': name, 'count': count, 'set': set, 'price': price, 'url': card_url})

    return cards

# Step 3: Write to CSV file
def download_csv(data, filename='decklist.csv'):
    headers = ['Deck Name', 'Card Name', 'Count', 'Set', 'Price (USD)', 'Card URL']

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for card in data:
            writer.writerow([card['deck_name'], card['name'], card['count'], card['set'], f"${card['price']:.2f}", card['url']])
    print(f"✅ Card lists saved to {filename}.")

def fetch_decks(urls):
    all_decks = []
    
    for url in urls:
        print(f"🟢 Fetching data from: {url}")
        decks = parse_deck_data(url)
        all_decks.extend(decks)
    
    return all_decks

# URLs for decks
deck_urls = [
    'https://limitlesstcg.com/decks?time=2324%2C2223&type=all&format=all&region=all&division=all&rank=cuts&page=1',
    'https://limitlesstcg.com/decks?time=2324%2C2223&type=all&format=all&region=all&division=all&rank=cuts&page=2',
]

# Fetch deck names from multiple pages
all_decks = fetch_decks(deck_urls)

# Store all card data
all_cards = []

# Loop through each deck and parse its cards
total_decks = len(all_decks)
for i, deck in enumerate(all_decks, start=1):
    deck_name = deck['name']
    deck_index = deck['index']
    url = f'https://limitlesstcg.com/decks/{deck_index}/cards'
    
    # Fetch and parse cards for the deck
    deck_cards = parse_decklist_cards(url, deck_name)
    all_cards.extend(deck_cards)

    print(f"🟢 Processing deck {i} of {total_decks}: {deck_name}")

# Save all card data to a CSV file
download_csv(all_cards)