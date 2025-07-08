import csv
import json

# Load inflation multipliers from CSV
def load_inflation_multipliers(csv_file):
    multipliers = {}
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            multipliers[int(row['year'])] = float(row['multiplier'])
    return multipliers

# Load commodity prices from JSON
def load_commodity_prices(json_file):
    with open(json_file) as f:
        return json.load(f)

# Convert historical currency to 2005 and 2017 values
def convert_to_2005_pounds(pounds, shillings=0, pence=0, year=1270, inflation_data=None):
    if year < 1971:
        total_old = pounds + (shillings / 20) + (pence / 240)
    else:
        total_old = pounds + (pence / 100)
    multiplier = inflation_data.get(year)
    if multiplier is None:
        raise ValueError(f"No inflation data for year {year}")
    value_2005 = total_old * multiplier
    value_2017 = value_2005 * 1.37
    return total_old, value_2005, value_2017

# Calculate historical buying power
def calculate_buying_power(total_old, year, commodity_data):
    commodities = commodity_data.get(str(year))
    if not commodities:
        raise ValueError(f"No commodity price data for year {year}")
    return {item: int(total_old // price) for item, price in commodities.items()}

# Example usage
if __name__ == "__main__":
    inflation_data = load_inflation_multipliers("inflation.csv")
    commodity_data = load_commodity_prices("commodities.json")

    pounds, shillings, pence, year = 1, 0, 0, 1270
    total_old, value_2005, value_2017 = convert_to_2005_pounds(
        pounds, shillings, pence, year, inflation_data
    )
    buying_power = calculate_buying_power(total_old, year, commodity_data)

    print(f"Original Value in {year}: £{total_old:.2f}")
    print(f"2005 Equivalent: £{value_2005:.2f}")
    print(f"2017 Equivalent: £{value_2017:.2f}")
    print(f"Buying Power in {year}:")
    for item, quantity in buying_power.items():
        print(f" - {quantity} {item}")
