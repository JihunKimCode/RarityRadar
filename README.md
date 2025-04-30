# RarityRadar
Analyze what impacts on card prices.

## Deadline & Submissions
* **May 2nd** - Poster, Notebook, and Code
* **May 9th** - 2-page Abstract

## Brief explanation of codes
* `fetchCardData.py`
  * Fetches *api.pokemontcg.io* to get information on cards in the sets specified in *set_ids*.
  * Takes information on cards from the folders specified in *folder_list*. To run this code, you should git clone [TCGdex Pricing History](https://github.com/tcgdex/price-history) in the proper directory.
* `graph.ipynb`creates various graphs using `merged_pokemon_data.csv`. It has scatterplots, boxplot graphs with line graphs, and line graphs.
* Metadecks
  * `cardlist scraper.py` scrapes webpage data of [Limitless](https://limitlesstcg.com/decks). Make sure you update *decks_list* properly.
  * `filterSets.py` filters the decklist.csv with *target_sets*. Outputs are saved in `filtered_cards.csv`.
* Artists
  * `fetchCardData_withArtist.py` works the same as `fetchCardData.py`, but it records artist information as well.
  * `graph_artist.ipynb` creates line graphs using `merged_pokemon_data_with_artist.csv`.

## Expansion Information
* SWSH1 = Sword & Shield (SSH)
* SWSH2 = Rebel Clash (RCL)
* SWSH3 = Darkness Ablaze (DAA)
* SWSH4 = Vivid Voltage (VIV)

## Datasets
### [Pokémon TCG Data](https://github.com/PokemonTCG/pokemon-tcg-data)

The first dataset organizes information on all Pokémon card games released so far by expansion unit. Most of the information comes from https://www.pokemon.com/us/pokemon-tcg/pokemon-cards, and information is added and modified through pull requests from many users. The dataset stores information on the name, type, battle information, rarity, image, and illustrator of the card in JSON format using numbers and characters. You can easily obtain information on each Pokémon card using 164 JSON files.

### [TCGdex Pricing History](https://github.com/tcgdex/price-history)

The second dataset organizes the price fluctuation trends of each Pokémon card by expansion pack unit. Most of the information comes from card trading sites such as TCGPlayer or eBay. The average price, lowest price, and highest price according to card status are stored in JSON format using numbers without decimal points. You can easily understand the price fluctuation trends of the card through 137 folders and the 10 to 100 JSON files in them.

### How to use datasets
Using these two data sets appropriately, we can analyze the correlation between rarity and price, or the factors that determine the price of a card, and through this, we can predict future card price movements. Both datasets can be processed easily using JSON.parse(). Also, the first dataset supports RESTful API as well, so we can get data using fetch.

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