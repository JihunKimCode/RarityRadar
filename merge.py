import pandas as pd

# Try reading with auto-delimiter first
cards_df = pd.read_csv("pokemon_cards.csv", encoding="ISO-8859-1")
averages_df = pd.read_csv("monthly_averages.csv", encoding="ISO-8859-1")

# Strip column names and split if needed
cards_df.columns = cards_df.columns.str.strip()
averages_df.columns = averages_df.columns.str.strip()

# If columns weren't parsed correctly (i.e., only one column), split manually
if cards_df.shape[1] == 1:
    cards_df = cards_df[cards_df.columns[0]].str.split(r'\0t|\,', expand=True)
    cards_df.columns = ["Set ID", "Number", "Name", "Rarity"]

if averages_df.shape[1] == 1:
    averages_df = averages_df[averages_df.columns[0]].str.split(r'\t|,', expand=True)
    averages_df.columns = ["Set ID", "Number", "Grade", "Month", "Average"]

# Merge the data
merged_df = averages_df.merge(cards_df, on=["Set ID", "Number"], how="left")

# Reorder columns
merged_df = merged_df[["Set ID", "Number", "Name", "Rarity", "Grade", "Month", "Average"]]

# Save to file
merged_df.to_csv("merged_pokemon_data.csv", index=False, sep=",", encoding="utf-8")

print("✅ Merged successfully!")
print(merged_df.head())
