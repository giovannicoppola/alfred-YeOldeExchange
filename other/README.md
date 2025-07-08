# YeOldeExchange
Can you create an alfred app that takes input in the format of 4 numbers, which correpond to pound, schillings, pence, and year, and runs the script below to return pound conversion and purchasing poiwer? 




I'll convert the script to use docopt for a proper command-line interface with arguments and help documentation.Perfect! I've converted the script to use docopt for a professional command-line interface. Here's what the enhanced version provides:

## Installation Requirements

First, you'll need to install docopt:

```bash
pip install docopt
```

## Command-Line Interface Features

### 1. **Multiple Commands**

- `convert` - Full currency conversion with inflation adjustment
- `purchasing` - Show purchasing power only
- `inflation` - Show inflation multipliers
- `items` - List available items and their prices
- `interactive` - Interactive mode

### 2. **Output Formats**

- `table` (default) - Formatted table output
- `json` - JSON format for programmatic use
- `csv` - CSV format for spreadsheets

### 3. **Command Examples**

```bash
# Basic conversion
./currency_converter.py convert 5 10 6 1850

# Convert to different target year
./currency_converter.py convert 1 0 0 1900 --target=2020

# Show purchasing power only
./currency_converter.py purchasing 2 5 0 1600

# Show purchasing power for specific item
./currency_converter.py purchasing 1 0 0 1400 --item=horse

# Get inflation multiplier
./currency_converter.py inflation 1750

# List item prices for a year
./currency_converter.py items --year=1600

# Interactive mode
./currency_converter.py interactive

# Get help
./currency_converter.py --help
```

### 4. **Output Formats**

**Table format (default):**

```
============================================================
Historical Currency Conversion
============================================================
Original Amount:    £5 10s 6d
Year:              1850
Decimal Pounds:    £5.53
Modern Equivalent: £441.75 (2017)
Inflation Factor:  80.0x

Purchasing Power:
------------------------------
  horses                    0.3
  cows                      0.5
  sheep                     3.7
  pigs                      4.6
============================================================
```

**JSON format:**

```bash
./currency_converter.py convert 1 0 0 1900 --format=json
```

**CSV format:**

```bash
./currency_converter.py convert 1 0 0 1900 --format=csv
```

### 5. **Error Handling**

- Validates input ranges (pounds 0-999, shillings 0-19, pence 0-11)
- Validates year range (1270-2017)
- Provides clear error messages
- Exits with appropriate error codes

### 6. **Help System**
Sure! Here's a Markdown document that clearly describes the conversion logic used by The National Archives currency converter:

---

```markdown
# 💷 The National Archives Currency Converter: Conversion Logic

This document outlines the logic used by [The National Archives UK Currency Converter](https://www.nationalarchives.gov.uk/currency/) to translate historical British currency into modern equivalents and compare historical purchasing power.

---

## 📐 1. Input Normalization

The converter accepts currency values from **1270 to 1970** using the **old British system**:

- **Pre-1971 (pre-decimal):**
  - 1 pound (£) = 20 shillings (s)
  - 1 shilling = 12 pence (d)
  - Therefore: 1 pound = 240 pence

  Formula:
  ```text
  total_old = pounds + (shillings / 20) + (pence / 240)
```

- **Post-1971 (decimal currency):**
    
    - 1 pound = 100 pence
        
    
    Formula:
    
    ```text
    total_old = pounds + (pence / 100)
    ```
    

---

## 📈 2. Convert to 2005 Pounds Using Historical Multipliers

Each year has a known **inflation multiplier** that converts historical currency to **2005 equivalents**. These multipliers are based on average prices and wages data for that year.

Example:

- £1 in 1270 ≈ £532.72 in 2005
    

Formula:

```text
value_2005 = total_old × inflation_multiplier_for_year
```

---

## ⏩ 3. Adjust to 2017 Pounds

To update the 2005 equivalent to 2017 values, the converter applies a flat **1.37 multiplier** (i.e., a 37% increase for inflation from 2005–2017):

```text
value_2017 = value_2005 × 1.37
```

---

## 🛒 4. Historical Buying Power (Optional Output)

The converter can optionally show how much of various goods (e.g. horses, cows, wool, wheat, labor) your historical currency could buy in that year. Prices for these items are based on historical data for each specific year.

Example (1270 data):

- Horse: £0.76
    
- Cow: £0.35
    
- Wool (1 stone): £0.13
    
- Wheat (1 quarter): £0.16
    
- Day’s wage (unskilled labor): £0.01
    

Formula:

```text
count_item = floor(total_old / item_price)
```

So £1 in 1270 could buy:

- ~1 horse
    
- ~2 cows
    
- ~7 stones of wool
    
- ~6 quarters of wheat
    
- ~100 days of labor
    

---

## 🔁 Summary of Steps

1. Convert input to decimal pounds using pre- or post-decimal logic.
    
2. Apply year-specific multiplier to get 2005 value.
    
3. Multiply by 1.37 to get 2017 value.
    
4. Optionally compute purchasing power based on historical commodity prices.
    

---

## 📚 Sources

- [The National Archives Currency Converter](https://www.nationalarchives.gov.uk/currency/)
    
- [GitHub – tna-currency-converter](https://github.com/nationalarchives/tna-currency-converter)
    

```

---

Let me know if you’d like this exported as a `.md` file or converted into a printable PDF.
```