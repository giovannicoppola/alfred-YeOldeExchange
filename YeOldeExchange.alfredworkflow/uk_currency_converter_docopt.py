#!/usr/bin/env python3
"""UK Historical Currency Converter

Usage:
    currency_converter.py convert <pounds> <shillings> <pence> <year> [--target=<year>] [--format=<type>]
    currency_converter.py purchasing <pounds> <shillings> <pence> <year> [--item=<item>]
    currency_converter.py inflation <year> [--target=<year>]
    currency_converter.py items [--year=<year>]
    currency_converter.py interactive
    currency_converter.py --help
    currency_converter.py --version

Commands:
    convert         Convert historical currency to modern equivalent
    purchasing      Show purchasing power for historical amount
    inflation       Show inflation multiplier for a year
    items           List available items and their prices
    interactive     Start interactive mode

Arguments:
    <pounds>        Number of pounds (0-999)
    <shillings>     Number of shillings (0-19)
    <pence>         Number of pence (0-11)
    <year>          Historical year (1270-2017)

Options:
    --target=<year>     Target year for comparison [default: 2017]
    --format=<type>     Output format: table, json, csv [default: table]
    --item=<item>       Show only specific item purchasing power
    --year=<year>       Year for item prices [default: 1500]
    -h --help           Show this help message
    --version           Show version

Examples:
    currency_converter.py convert 5 10 6 1850
    currency_converter.py convert 1 0 0 1900 --target=2020
    currency_converter.py purchasing 2 5 0 1600
    currency_converter.py purchasing 1 0 0 1400 --item=horse
    currency_converter.py inflation 1750
    currency_converter.py items --year=1600
    currency_converter.py interactive

Available items for purchasing power:
    horse, cow, sheep, pig, wheat_quarter, wool_stone, bread_loaf, ale_gallon
"""

import json
import csv
import sys
from datetime import datetime
from typing import Dict, Tuple, Optional, List
from docopt import docopt

__version__ = "1.0.0"

class UKCurrencyConverter:
    def __init__(self):
        """Initialize the converter with historical data approximations"""
        
        # Pre-1971 currency system: 1 pound = 20 shillings = 240 pence
        self.old_currency_system = {
            'pounds_to_shillings': 20,
            'shillings_to_pence': 12,
            'pounds_to_pence': 240
        }
        
        # Approximate inflation multipliers based on historical data
        # These are estimated values - the actual National Archives uses more precise data
        self.inflation_data = self._load_inflation_data()
        
        # Historical commodity prices (approximate values in pounds/shillings/pence)
        self.historical_prices = self._load_historical_prices()
        
        # Base year for modern comparison (National Archives uses 2017)
        self.base_year = 2017
        
    def _load_inflation_data(self) -> Dict[int, float]:
        """
        Load approximate inflation multipliers to convert to 2017 values
        These are rough approximations based on historical price indices
        """
        # Sample data points - in reality, this would be a comprehensive dataset
        # Values represent multipliers to convert to 2017 purchasing power
        inflation_multipliers = {
            1270: 1000.0,    # Very rough medieval approximation
            1300: 800.0,
            1400: 600.0,
            1500: 400.0,
            1600: 200.0,
            1700: 150.0,
            1750: 120.0,
            1800: 100.0,
            1850: 80.0,
            1900: 60.0,
            1910: 50.0,
            1920: 25.0,
            1930: 35.0,
            1940: 30.0,
            1950: 25.0,
            1960: 20.0,
            1970: 15.0,
            1971: 14.8,     # Decimalization year
            1980: 5.0,
            1990: 2.5,
            2000: 1.8,
            2010: 1.3,
            2017: 1.0       # Base year
        }
        
        return inflation_multipliers
    
    def _load_historical_prices(self) -> Dict[str, Dict[int, float]]:
        """
        Load historical prices for various commodities in decimal pounds
        Based on historical records and archaeological evidence
        """
        # Prices are approximate and based on historical records
        # Values are in decimal pounds equivalent
        historical_prices = {
            'horse': {
                1300: 1.5,    # £1 10s - working horse
                1400: 2.0,    # £2 - good riding horse
                1500: 3.0,    # £3 - quality horse
                1600: 4.0,    # £4 - good horse
                1700: 6.0,    # £6 - riding horse
                1800: 15.0,   # £15 - good horse
                1850: 20.0,   # £20 - riding horse
                1900: 25.0,   # £25 - good horse
                1950: 50.0,   # £50 - horse
            },
            'cow': {
                1300: 0.5,    # 10s - dairy cow
                1400: 0.75,   # 15s - good cow
                1500: 1.0,    # £1 - cow
                1600: 1.5,    # £1 10s - good cow
                1700: 2.0,    # £2 - dairy cow
                1800: 8.0,    # £8 - good cow
                1850: 12.0,   # £12 - dairy cow
                1900: 15.0,   # £15 - good cow
                1950: 30.0,   # £30 - cow
            },
            'sheep': {
                1300: 0.08,   # 2s - sheep
                1400: 0.1,    # 2s - sheep
                1500: 0.15,   # 3s - sheep
                1600: 0.2,    # 4s - sheep
                1700: 0.3,    # 6s - sheep
                1800: 1.0,    # £1 - sheep
                1850: 1.5,    # £1 10s - sheep
                1900: 2.0,    # £2 - sheep
                1950: 4.0,    # £4 - sheep
            },
            'pig': {
                1300: 0.05,   # 1s - pig
                1400: 0.08,   # 1s 6d - pig
                1500: 0.1,    # 2s - pig
                1600: 0.15,   # 3s - pig
                1700: 0.25,   # 5s - pig
                1800: 0.8,    # 16s - pig
                1850: 1.2,    # £1 4s - pig
                1900: 1.5,    # £1 10s - pig
                1950: 3.0,    # £3 - pig
            },
            'wheat_quarter': {  # Quarter = 8 bushels
                1300: 0.3,    # 6s - quarter of wheat
                1400: 0.25,   # 5s - quarter of wheat
                1500: 0.3,    # 6s - quarter of wheat
                1600: 0.4,    # 8s - quarter of wheat
                1700: 0.5,    # 10s - quarter of wheat
                1800: 2.0,    # £2 - quarter of wheat
                1850: 2.5,    # £2 10s - quarter of wheat
                1900: 1.5,    # £1 10s - quarter of wheat
                1950: 3.0,    # £3 - quarter of wheat
            },
            'wool_stone': {  # Stone = 14 pounds weight
                1300: 0.5,    # 10s - stone of wool
                1400: 0.4,    # 8s - stone of wool
                1500: 0.6,    # 12s - stone of wool
                1600: 0.8,    # 16s - stone of wool
                1700: 1.0,    # £1 - stone of wool
                1800: 2.0,    # £2 - stone of wool
                1850: 2.5,    # £2 10s - stone of wool
                1900: 2.0,    # £2 - stone of wool
                1950: 4.0,    # £4 - stone of wool
            },
            'bread_loaf': {
                1300: 0.001,  # 1/4d - loaf of bread
                1400: 0.002,  # 1/2d - loaf of bread
                1500: 0.003,  # 3/4d - loaf of bread
                1600: 0.004,  # 1d - loaf of bread
                1700: 0.008,  # 2d - loaf of bread
                1800: 0.02,   # 5d - loaf of bread
                1850: 0.03,   # 7d - loaf of bread
                1900: 0.025,  # 6d - loaf of bread
                1950: 0.05,   # 1s - loaf of bread
            },
            'ale_gallon': {
                1300: 0.01,   # 2d - gallon of ale
                1400: 0.01,   # 2d - gallon of ale
                1500: 0.015,  # 3d - gallon of ale
                1600: 0.02,   # 4d - gallon of ale
                1700: 0.025,  # 6d - gallon of ale
                1800: 0.05,   # 1s - gallon of ale
                1850: 0.08,   # 1s 6d - gallon of ale
                1900: 0.1,    # 2s - gallon of ale
                1950: 0.2,    # 4s - gallon of ale
            }
        }
        
        return historical_prices
    
    def get_historical_price(self, item: str, year: int) -> float:
        """
        Get historical price for an item in a given year
        Uses interpolation for years not in the dataset
        """
        if item not in self.historical_prices:
            raise ValueError(f"Item '{item}' not found in historical prices")
        
        item_prices = self.historical_prices[item]
        
        if year in item_prices:
            return item_prices[year]
        
        # Find the closest years for interpolation
        years = sorted(item_prices.keys())
        
        if year < min(years):
            return item_prices[min(years)]
        if year > max(years):
            return item_prices[max(years)]
        
        # Linear interpolation
        for i in range(len(years) - 1):
            if years[i] <= year <= years[i + 1]:
                lower_year, upper_year = years[i], years[i + 1]
                lower_price, upper_price = item_prices[lower_year], item_prices[upper_year]
                
                # Linear interpolation formula
                ratio = (year - lower_year) / (upper_year - lower_year)
                return lower_price + ratio * (upper_price - lower_price)
        
        return 0.0  # Fallback
    
    def parse_old_currency(self, pounds: int = 0, shillings: int = 0, pence: int = 0) -> float:
        """
        Convert old UK currency (£sd) to decimal pounds
        
        Args:
            pounds: Number of pounds
            shillings: Number of shillings (0-19)
            pence: Number of pence (0-11)
            
        Returns:
            Decimal pounds equivalent
        """
        if shillings >= 20:
            raise ValueError("Shillings must be less than 20")
        if pence >= 12:
            raise ValueError("Pence must be less than 12")
            
        # Convert everything to old pence first
        total_old_pence = (pounds * self.old_currency_system['pounds_to_pence'] + 
                          shillings * self.old_currency_system['shillings_to_pence'] + 
                          pence)
        
        # Convert old pence to decimal pounds (240 old pence = 1 pound)
        decimal_pounds = total_old_pence / self.old_currency_system['pounds_to_pence']
        
        return decimal_pounds
    
    def get_inflation_multiplier(self, year: int) -> float:
        """
        Get inflation multiplier for a given year
        Uses interpolation for years not in the dataset
        """
        if year in self.inflation_data:
            return self.inflation_data[year]
        
        # Find the closest years for interpolation
        years = sorted(self.inflation_data.keys())
        
        if year < min(years):
            return self.inflation_data[min(years)]
        if year > max(years):
            return self.inflation_data[max(years)]
        
        # Linear interpolation
        for i in range(len(years) - 1):
            if years[i] <= year <= years[i + 1]:
                lower_year, upper_year = years[i], years[i + 1]
                lower_mult, upper_mult = self.inflation_data[lower_year], self.inflation_data[upper_year]
                
                # Linear interpolation formula
                ratio = (year - lower_year) / (upper_year - lower_year)
                return lower_mult + ratio * (upper_mult - lower_mult)
        
        return 1.0  # Fallback
    
    def convert_to_modern(self, amount: float, year: int, target_year: int = 2017) -> float:
        """
        Convert historical amount to modern purchasing power
        
        Args:
            amount: Amount in decimal pounds
            year: Historical year
            target_year: Target year for conversion (default 2017)
            
        Returns:
            Modern equivalent value
        """
        if year < 1270 or year > 2017:
            raise ValueError("Year must be between 1270 and 2017")
        
        multiplier = self.get_inflation_multiplier(year)
        target_multiplier = self.get_inflation_multiplier(target_year)
        
        # Adjust multiplier relative to target year
        adjusted_multiplier = multiplier / target_multiplier
        
        return amount * adjusted_multiplier
    
    def calculate_purchasing_power(self, amount: float, year: int, specific_item: str = None) -> Dict[str, float]:
        """
        Calculate what the amount could purchase in terms of historical goods
        
        Args:
            amount: Amount in decimal pounds
            year: Historical year
            specific_item: If specified, show only this item
            
        Returns:
            Dictionary with quantities of various items that could be purchased
        """
        purchasing_power = {}
        
        available_items = {
            'horses': 'horse',
            'cows': 'cow', 
            'sheep': 'sheep',
            'pigs': 'pig',
            'quarters_of_wheat': 'wheat_quarter',
            'stones_of_wool': 'wool_stone',
            'loaves_of_bread': 'bread_loaf',
            'gallons_of_ale': 'ale_gallon'
        }
        
        # If specific item requested, filter to just that item
        if specific_item:
            if specific_item in available_items.values():
                # Find display name for the item
                display_name = None
                for display, item_key in available_items.items():
                    if item_key == specific_item:
                        display_name = display
                        break
                if display_name:
                    available_items = {display_name: specific_item}
                else:
                    available_items = {}
            else:
                available_items = {}
        
        for display_name, item_key in available_items.items():
            try:
                item_price = self.get_historical_price(item_key, year)
                if item_price > 0:
                    quantity = amount / item_price
                    purchasing_power[display_name] = quantity
            except ValueError:
                continue
        
        return purchasing_power
    
    def convert_historical_currency(self, pounds: int = 0, shillings: int = 0, 
                                  pence: int = 0, year: int = 1900, 
                                  target_year: int = 2017) -> Dict[str, float]:
        """
        Complete conversion from historical UK currency to modern values
        
        Args:
            pounds: Historical pounds
            shillings: Historical shillings
            pence: Historical pence
            year: Year of the historical amount
            target_year: Target year for modern comparison
            
        Returns:
            Dictionary with conversion results
        """
        # Stage 1: Convert old currency to decimal
        decimal_amount = self.parse_old_currency(pounds, shillings, pence)
        
        # Stage 2: Apply inflation adjustment
        modern_value = self.convert_to_modern(decimal_amount, year, target_year)
        
        # Stage 3: Calculate purchasing power
        purchasing_power = self.calculate_purchasing_power(decimal_amount, year)
        
        return {
            'original_amount': f"£{pounds} {shillings}s {pence}d",
            'decimal_pounds': decimal_amount,
            'year': year,
            'modern_equivalent': modern_value,
            'target_year': target_year,
            'inflation_multiplier': self.get_inflation_multiplier(year),
            'purchasing_power': purchasing_power
        }
    
    def get_available_items(self) -> List[str]:
        """Get list of available items for purchasing power calculations"""
        return list(self.historical_prices.keys())
    
    def format_purchasing_power(self, purchasing_power: Dict[str, float]) -> str:
        """Format purchasing power results as a readable string"""
        if not purchasing_power:
            return "No purchasing power data available"
        
        items = []
        for item, quantity in purchasing_power.items():
            if quantity >= 1:
                items.append(f"{quantity:.1f} {item}")
            elif quantity >= 0.1:
                items.append(f"{quantity:.2f} {item}")
            else:
                items.append(f"{quantity:.3f} {item}")
        
        return " OR ".join(items)
    
    def format_currency(self, amount: float) -> str:
        """Format amount as currency string"""
        return f"£{amount:,.2f}"

class OutputFormatter:
    """Handle different output formats"""
    
    @staticmethod
    def format_table(result: Dict) -> str:
        """Format result as table"""
        output = []
        output.append("=" * 60)
        output.append(f"Historical Currency Conversion")
        output.append("=" * 60)
        output.append(f"Original Amount:    {result['original_amount']}")
        output.append(f"Year:              {result['year']}")
        output.append(f"Decimal Pounds:    £{result['decimal_pounds']:.2f}")
        output.append(f"Modern Equivalent: £{result['modern_equivalent']:,.2f} ({result['target_year']})")
        output.append(f"Inflation Factor:  {result['inflation_multiplier']:.1f}x")
        
        if 'purchasing_power' in result and result['purchasing_power']:
            output.append("")
            output.append("Purchasing Power:")
            output.append("-" * 30)
            converter = UKCurrencyConverter()
            for item, quantity in result['purchasing_power'].items():
                if quantity >= 1:
                    output.append(f"  {item:20} {quantity:8.1f}")
                elif quantity >= 0.1:
                    output.append(f"  {item:20} {quantity:8.2f}")
                else:
                    output.append(f"  {item:20} {quantity:8.3f}")
        
        output.append("=" * 60)
        return "\n".join(output)
    
    @staticmethod
    def format_json(result: Dict) -> str:
        """Format result as JSON"""
        return json.dumps(result, indent=2)
    
    @staticmethod
    def format_csv(result: Dict) -> str:
        """Format result as CSV"""
        output = []
        output.append("field,value")
        output.append(f"original_amount,{result['original_amount']}")
        output.append(f"year,{result['year']}")
        output.append(f"decimal_pounds,{result['decimal_pounds']:.2f}")
        output.append(f"modern_equivalent,{result['modern_equivalent']:.2f}")
        output.append(f"target_year,{result['target_year']}")
        output.append(f"inflation_multiplier,{result['inflation_multiplier']:.1f}")
        
        if 'purchasing_power' in result and result['purchasing_power']:
            for item, quantity in result['purchasing_power'].items():
                output.append(f"purchasing_power_{item},{quantity:.3f}")
        
        return "\n".join(output)

def run_convert_command(args, converter):
    """Handle convert command"""
    try:
        pounds = int(args['<pounds>'])
        shillings = int(args['<shillings>'])
        pence = int(args['<pence>'])
        year = int(args['<year>'])
        target_year = int(args['--target'])
        format_type = args['--format']
        
        if pounds < 0 or pounds > 999:
            raise ValueError("Pounds must be between 0 and 999")
        if shillings < 0 or shillings > 19:
            raise ValueError("Shillings must be between 0 and 19")
        if pence < 0 or pence > 11:
            raise ValueError("Pence must be between 0 and 11")
        if year < 1270 or year > 2017:
            raise ValueError("Year must be between 1270 and 2017")
        
        result = converter.convert_historical_currency(pounds, shillings, pence, year, target_year)
        
        if format_type == 'json':
            print(OutputFormatter.format_json(result))
        elif format_type == 'csv':
            print(OutputFormatter.format_csv(result))
        else:
            print(OutputFormatter.format_table(result))
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def run_purchasing_command(args, converter):
    """Handle purchasing command"""
    try:
        pounds = int(args['<pounds>'])
        shillings = int(args['<shillings>'])
        pence = int(args['<pence>'])
        year = int(args['<year>'])
        specific_item = args['--item']
        
        if pounds < 0 or pounds > 999:
            raise ValueError("Pounds must be between 0 and 999")
        if shillings < 0 or shillings > 19:
            raise ValueError("Shillings must be between 0 and 19")
        if pence < 0 or pence > 11:
            raise ValueError("Pence must be between 0 and 11")
        if year < 1270 or year > 2017:
            raise ValueError("Year must be between 1270 and 2017")
        
        decimal_amount = converter.parse_old_currency(pounds, shillings, pence)
        purchasing_power = converter.calculate_purchasing_power(decimal_amount, year, specific_item)
        
        print(f"Purchasing power of £{pounds} {shillings}s {pence}d in {year}:")
        print("-" * 50)
        
        if purchasing_power:
            for item, quantity in purchasing_power.items():
                if quantity >= 1:
                    print(f"{item:20} {quantity:8.1f}")
                elif quantity >= 0.1:
                    print(f"{item:20} {quantity:8.2f}")
                else:
                    print(f"{item:20} {quantity:8.3f}")
        else:
            print("No purchasing power data available")
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def run_inflation_command(args, converter):
    """Handle inflation command"""
    try:
        year = int(args['<year>'])
        target_year = int(args['--target'])
        
        if year < 1270 or year > 2017:
            raise ValueError("Year must be between 1270 and 2017")
        
        multiplier = converter.get_inflation_multiplier(year)
        target_multiplier = converter.get_inflation_multiplier(target_year)
        relative_multiplier = multiplier / target_multiplier
        
        print(f"Inflation data for {year}:")
        print(f"  Multiplier to {target_year}: {relative_multiplier:.1f}x")
        print(f"  £1 in {year} = £{relative_multiplier:.2f} in {target_year}")
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def run_items_command(args, converter):
    """Handle items command"""
    try:
        year = int(args['--year'])
        
        if year < 1270 or year > 2017:
            raise ValueError("Year must be between 1270 and 2017")
        
        print(f"Historical prices in {year}:")
        print("-" * 40)
        
        for item in converter.get_available_items():
            try:
                price = converter.get_historical_price(item, year)
                print(f"{item:20} £{price:.3f}")
            except ValueError:
                print(f"{item:20} No data")
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def run_interactive_mode(converter):
    """Run interactive mode"""
    print("UK Historical Currency Converter - Interactive Mode")
    print("=" * 50)
    print("Enter 'quit' or 'exit' to leave")
    print()
    
    while True:
        try:
            print("Enter historical amount:")
            pounds_input = input("  Pounds (0-999): ").strip()
            if pounds_input.lower() in ['quit', 'exit']:
                break
            pounds = int(pounds_input or "0")
            
            shillings_input = input("  Shillings (0-19): ").strip()
            if shillings_input.lower() in ['quit', 'exit']:
                break
            shillings = int(shillings_input or "0")
            
            pence_input = input("  Pence (0-11): ").strip()
            if pence_input.lower() in ['quit', 'exit']:
                break
            pence = int(pence_input or "0")
            
            year_input = input("  Year (1270-2017): ").strip()
            if year_input.lower() in ['quit', 'exit']:
                break
            year = int(year_input)
            
            result = converter.convert_historical_currency(pounds, shillings, pence, year)
            print("\n" + OutputFormatter.format_table(result))
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except ValueError as e:
            print(f"Error: {e}")
            print()
        except EOFError:
            print("\nGoodbye!")
            break

def main():
    """Main entry point"""
    args = docopt(__doc__, version=f"UK Historical Currency Converter {__version__}")
    
    converter = UKCurrencyConverter()
    
    try:
        if args['convert']:
            run_convert_command(args, converter)
        elif args['purchasing']:
            run_purchasing_command(args, converter)
        elif args['inflation']:
            run_inflation_command(args, converter)
        elif args['items']:
            run_items_command(args, converter)
        elif args['interactive']:
            run_interactive_mode(converter)
        else:
            print(__doc__)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
