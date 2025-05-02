# RarityRadar

## Motivation
* Card market prices constantly fluctuate, making it difficult to invest confidently. Due to our mutual interest in card games, we devised a way to solve this problem in the Pokémon TCG.
* We first determined whether rarity alone contributed to the price. Then, the project was expanded to determine what other factors affected the price.

## Setup Instruction
1. Download and Install Python 3.8+
2. Clone the Repository: `git clone https://github.com/JihunKimCode/RarityRadar.git`
3. Feel free to use VS Code or Jupyter Notebook, depending on your preference.
4. Make sure the following are installed properly: pandas, matplotlib, seaborn, numpy, beautifulSoup, requests, and PySpark. Try `pip install -r requirements.txt`.
5. If you are not sure which code to run, read the **Brief explanation of codes** below.

## Brief explanation of codes
* `fetchCardData.py`
  * Fetches *api.pokemontcg.io* to get information on cards in the sets specified in *set_ids* list (Dataset: Pokémon TCG Data).
  * Takes information on cards from the folders specified in the *folders* list (Dataset: TCGdex Pricing History).
  * To run this code, you should git clone [TCGdex Pricing History](https://github.com/tcgdex/price-history) in the proper directory.
* `graph.ipynb`
  * Creates various graphs using `merged_pokemon_data.csv` and `Metadecks/filtered_cards.csv`. Make sure you have those CSVs before you run this.
    * You should run `fetchCardData.py`, `Metadecks/cardlist scraper.py`, and `Metadecks/filterSets.py` to get these CSVs.
  * Creates heatmaps, scatterplots, boxplots, and linegraphs. Also, it establishes K-means clustering using Spark. 
* `Metadecks/cardlist scraper.py` scrapes webpage data of [Limitless](https://limitlesstcg.com/decks). Make sure you update *deck_urls* properly.
* `Metadecks/filterSets.py` filters the `decklist.csv` with *target_sets*.
* `Artists/fetchCardData_withArtist.py` works the same as `fetchCardData.py`, but it records artist information as well.
* `Artists/graph_artist.ipynb` creates line graphs using `merged_pokemon_data_with_artist.csv`.

## Expansion Information
* SWSH1 = Sword & Shield (SSH)
* SWSH2 = Rebel Clash (RCL)
* SWSH3 = Darkness Ablaze (DAA)
* SWSH4 = Vivid Voltage (VIV)
* SWSH5 = Battle Styles (BST)

## Datasets
### [Pokémon TCG Data](https://github.com/PokemonTCG/pokemon-tcg-data)

This dataset organizes information on all Pokémon card games released so far by expansion unit. Most of the information comes from https://www.pokemon.com/us/pokemon-tcg/pokemon-cards, and information is added and modified through pull requests from many users. The dataset stores information on the name, type, battle information, rarity, image, and illustrator of the card in JSON format using numbers and characters. You can easily obtain information on each Pokémon card using 164 JSON files.

### [TCGdex Pricing History](https://github.com/tcgdex/price-history)

This dataset organizes the price fluctuation trends of each Pokémon card by expansion pack unit. Most of the information comes from card trading sites such as TCGPlayer or eBay. The average price, lowest price, and highest price according to card status are stored in JSON format using numbers without decimal points. You can easily understand the price fluctuation trends of the card through 137 folders and the 10 to 100 JSON files in them.

### How to use datasets
Using these two data sets appropriately, we can analyze the correlation between rarity and price, or the factors that determine the price of a card, and through this, we can predict future card price movements.  Also, the first dataset supports RESTful API as well, so we can get data using fetch.

### Additional Sources
* [Pokémon TCG Data - documentation](https://docs.pokemontcg.io/)
* [Pokémon TCG Data - JSON without query](https://api.pokemontcg.io/v2/cards)
  * Search card: append `?q=name:${query}`
  * Search expansion: append `?q=set.id:${expansion id}` or `?q=set.name:${expansion name}`
* [Pokémon Card Searcher](https://jihunkimcode.github.io/Pokemon-Card-Searcher/)
  * This webpage makes it easier to search for card information in Pokémon TCG Data.
  * Open `DevTools Inspect mode` > `Console` > Enter `cachedData` to see JSON data of each cards.
* [Limitless](https://limitlesstcg.com/decks)
  * This webpage contains information of meta decks.
  * Using filters, we can set time range.
