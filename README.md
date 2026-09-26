# Ye Olde Exchange - Alfred Workflow

A powerful Alfred workflow for converting historical UK currency to modern values and calculating purchasing power.

<a href="https://github.com/giovannicoppola/alfred-YeOldeExchange/releases/latest/">
<img alt="Downloads"
src="https://img.shields.io/github/downloads/giovannicoppola/alfred-YeOldeExchange/total?color=purple&label=Downloads"><br/>
</a>

## 🎯 What It Does

Convert historical UK currency (pounds, shillings, pence) from any year between 1270-2017 to modern equivalent values, plus see what that money could buy in that historical period.



## 🚀 Usage

1. **Open Alfred:** Press ⌘ + Space (or your configured hotkey)

2. **Type the command:** `yeolde` followed by 4 numbers:
   - **Pounds** (0-999)
   - **Shillings** (0-19) 
   - **Pence** (0-11)
   - **Year** (1270-2017)

### Examples

```
yeolde 5 10 6 1850
```
Converts £5 10s 6d from 1850
- Result: £442.00 in 2017 money (80x inflation)
- Could buy: horses, cows, sheep, etc.

```
yeolde 1 0 0 1600
```
Converts £1 from 1600
- Result: £200.00 in 2017 money (200x inflation)

```
yeolde 2 5 8 1400
```
Converts £2 5s 8d from 1400

## 📊 Output

The workflow shows multiple results:

1. **💰 Main Conversion**
   - Original amount → Modern equivalent
   - Inflation multiplier

2. **🛒 Purchasing Power Summary**
   - What the money could buy (top items)

3. **📝 Individual Items**
   - Specific quantities of historical goods
   - Horses, cows, sheep, pigs, wheat, wool, bread, ale

4. **📋 Copy to Clipboard**
   - Press Enter on any result to copy it

## 💡 Understanding the Results

### Currency System (Pre-1971)
- **1 pound (£)** = 20 shillings (s)
- **1 shilling** = 12 pence (d)
- **Total:** 1 pound = 240 pence

### Historical Items Include:
- **Animals:** Horses, cows, sheep, pigs
- **Commodities:** Quarters of wheat, stones of wool
- **Daily goods:** Loaves of bread, gallons of ale

### Example Output:
```
£5 10s 6d in 1850 = £442.00 in 2017 (80.0x inflation)
Could buy: 0.28 horses OR 0.46 cows OR 3.7 sheep
```

## ⚙️ Technical Details

### Files in Workflow:
- `info.plist` - Alfred workflow configuration
- `currency_converter.py` - Main Alfred interface script
- `uk_currency_converter_docopt.py` - Core conversion engine
- `README.md` - Documentation

### Requirements:
- **Alfred 4+** with Powerpack
- **Python 3** (usually pre-installed on macOS)
- **docopt package** (`pip3 install --user --break-system-packages docopt`)

### Data Sources:
- Historical inflation data approximations
- Archaeological and historical price records
- National Archives methodologies

## 🐛 Troubleshooting

### "No module named 'docopt'" Error:
```bash
pip3 install --user --break-system-packages docopt
```

### "Invalid Input" Messages:
- Check that you're entering exactly 4 numbers
- Verify ranges: pounds (0-999), shillings (0-19), pence (0-11), year (1270-2017)

### Workflow Not Appearing:
- Make sure Alfred Powerpack is installed
- Check Alfred Preferences → Workflows tab
- Verify Python 3 is accessible in Terminal

### Permission Issues:
```bash
cd YeOldeExchange.alfredworkflow
chmod +x currency_converter.py uk_currency_converter_docopt.py
```

## 📚 Historical Context

This tool uses approximated historical data. The actual National Archives maintains more precise datasets, but these approximations provide educational insights into:

- **Medieval economy** (1270-1500): Very high inflation multipliers
- **Early modern period** (1500-1700): Gradual price changes  
- **Industrial revolution** (1700-1900): Significant economic shifts
- **Modern era** (1900-2017): Accelerating inflation

## 🎨 Customization

### Adding an Icon:
1. Create a 512x512 PNG icon
2. Save as `icon.png` in the workflow folder
3. Reimport the workflow

### Modifying Output Format:
Edit `currency_converter.py` to change:
- Number of items shown
- Formatting of results
- Additional purchasing power calculations

## 📄 License

- This workflow is based on the historical currency converter script and is provided for educational purposes.
- Icons from flaticon.com

## 🔧 Version

**0.0.1** - Initial release with full conversion and purchasing power features

# Changelog
- 2026-07-21: version 0.0.2, fixed the backend script path so conversion works regardless of the launch directory
