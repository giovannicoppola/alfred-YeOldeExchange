# Ye Olde Exchange - Alfred Workflow

Historical UK Currency Converter for Alfred

## Description

Convert historical UK currency (pounds, shillings, pence) to modern equivalent values and see purchasing power comparisons.

## Installation

1. Double-click the `YeOldeExchange.alfredworkflow` file to install it in Alfred
2. Make sure you have Python 3 installed with the `docopt` package:
   ```bash
   pip3 install docopt
   ```

## Usage

1. Open Alfred (⌘ + Space)
2. Type `yeolde` followed by 4 numbers:
   - Pounds (0-999)
   - Shillings (0-19)
   - Pence (0-11)
   - Year (1270-2017)

### Examples

- `yeolde 5 10 6 1850` - Convert £5 10s 6d from 1850
- `yeolde 1 0 0 1900` - Convert £1 from 1900
- `yeolde 2 5 8 1600` - Convert £2 5s 8d from 1600

## Output

The workflow will show:
1. **Modern equivalent** - What the amount is worth in 2017 money
2. **Purchasing power** - What the amount could buy in that historical period
3. **Individual items** - Specific quantities of goods the money could purchase

Press Enter on any result to copy it to your clipboard.

## Currency System

Before 1971, the UK used:
- 1 pound (£) = 20 shillings (s)
- 1 shilling = 12 pence (d)
- So 1 pound = 240 pence

## Historical Items

The purchasing power calculation includes:
- Horses, cows, sheep, pigs
- Quarters of wheat, stones of wool
- Loaves of bread, gallons of ale

## Requirements

- Alfred with Powerpack
- Python 3
- docopt package (`pip3 install docopt`)

## Version

1.0.0 