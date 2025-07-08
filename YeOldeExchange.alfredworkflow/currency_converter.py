#!/usr/bin/env python3

import sys
import json
import subprocess
import os
import re

def debug_log(message):
    """Log debug messages to stderr for Alfred debugger"""
    print(f"[DEBUG] {message}", file=sys.stderr)

def get_icon_for_item(item_key):
    """Get the appropriate icon file for a purchasing power item"""
    icon_mapping = {
        'horses': 'icons/horse.png',
        'cows': 'icons/cow.png',
        'sheep': 'icons/sheep.png',
        'pigs': 'icons/pig.png',
        'quarters_of_wheat': 'icons/wheat.png',
        'stones_of_wool': 'icons/wool.png',
        'loaves_of_bread': 'icons/bread.png',
        'gallons_of_ale': 'icons/ale.png'
    }
    return icon_mapping.get(item_key, "icon.png")  # Default to main icon if not found

def format_currency(amount):
    """Format currency amount"""
    return f"£{amount:,.2f}"

def format_purchasing_power(purchasing_power):
    """Format purchasing power as readable string"""
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
    
    if len(items) <= 3:
        return " OR ".join(items)
    else:
        return " OR ".join(items[:3]) + f" OR {len(items)-3} more items..."

def parse_input(query):
    """Parse Alfred input into pounds, shillings, pence, year"""
    debug_log(f"Input query: '{query}'")
    
    if not query.strip():
        debug_log("Empty query received")
        return None, "Enter 4 numbers: pounds shillings pence year"
    
    # Split by spaces and filter out empty strings
    parts = [p.strip() for p in query.split() if p.strip()]
    debug_log(f"Parsed parts: {parts}")
    
    if len(parts) < 4:
        debug_log(f"Insufficient parts: got {len(parts)}, need 4")
        return None, f"Need 4 numbers, got {len(parts)}. Format: pounds shillings pence year"
    
    try:
        pounds = int(parts[0])
        shillings = int(parts[1])
        pence = int(parts[2])
        year = int(parts[3])
        
        debug_log(f"Parsed values: pounds={pounds}, shillings={shillings}, pence={pence}, year={year}")
        
        # Validate ranges
        if pounds < 0 or pounds > 999:
            debug_log(f"Invalid pounds: {pounds}")
            return None, "Pounds must be between 0 and 999"
        if shillings < 0 or shillings > 19:
            debug_log(f"Invalid shillings: {shillings}")
            return None, "Shillings must be between 0 and 19"
        if pence < 0 or pence > 11:
            debug_log(f"Invalid pence: {pence}")
            return None, "Pence must be between 0 and 11"
        if year < 1270 or year > 2017:
            debug_log(f"Invalid year: {year}")
            return None, "Year must be between 1270 and 2017"
        
        debug_log("Input validation passed")
        return (pounds, shillings, pence, year), None
        
    except ValueError as e:
        debug_log(f"ValueError parsing input: {e}")
        return None, "All inputs must be numbers"

def call_converter(pounds, shillings, pence, year):
    """Call the docopt currency converter script"""
    try:
        # Get the path to the original script
        script_path = 'uk_currency_converter_docopt.py'
        
        debug_log(f"Script path: {script_path}")
        debug_log(f"Script exists: {os.path.exists(script_path)}")
        
        # Call the script with convert command
        cmd = [
            'python3', script_path, 'convert', 
            str(pounds), str(shillings), str(pence), str(year),
            '--format=json'
        ]
        
        debug_log(f"Command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        debug_log(f"Return code: {result.returncode}")
        debug_log(f"Stdout: {result.stdout[:200]}...")  # First 200 chars
        debug_log(f"Stderr: {result.stderr}")
        
        if result.returncode != 0:
            error_msg = f"Converter error: {result.stderr.strip()}"
            debug_log(error_msg)
            return None, error_msg
        
        # Parse JSON output
        data = json.loads(result.stdout)
        debug_log("JSON parsing successful")
        return data, None
        
    except subprocess.TimeoutExpired:
        debug_log("Subprocess timeout")
        return None, "Conversion timed out"
    except json.JSONDecodeError as e:
        debug_log(f"JSON decode error: {e}")
        debug_log(f"Raw stdout: {result.stdout}")
        return None, f"Invalid JSON from converter: {e}"
    except Exception as e:
        debug_log(f"Unexpected error in call_converter: {e}")
        return None, f"Error calling converter: {e}"

def create_alfred_items(query):
    """Create Alfred JSON response"""
    debug_log("Starting create_alfred_items")
    items = []
    
    # Parse the input
    parsed, error = parse_input(query)
    
    if error:
        debug_log(f"Input parsing failed: {error}")
        items.append({
            "uid": "error",
            "title": "Invalid Input",
            "subtitle": error,
            "arg": "",
            "valid": False,
            "icon": {
                "type": "default",
                "path": "icon.png"
            }
        })
        return {"items": items}
    
    pounds, shillings, pence, year = parsed
    debug_log(f"Successfully parsed input: {pounds}£ {shillings}s {pence}d {year}")
    
    # Call the converter
    result, error = call_converter(pounds, shillings, pence, year)
    
    if error:
        debug_log(f"Converter call failed: {error}")
        items.append({
            "uid": "converter_error",
            "title": "Conversion Error",
            "subtitle": error,
            "arg": "",
            "valid": False,
            "icon": {
                "type": "default",
                "path": "icon.png"
            }
        })
        return {"items": items}
    
    debug_log("Converter call successful, building Alfred items")
    
    # Create main conversion result item
    original = result['original_amount']
    modern = format_currency(result['modern_equivalent'])
    multiplier = result['inflation_multiplier']
    
    conversion_text = f"{original} in {year} = {modern} in {result['target_year']} ({multiplier:.1f}x inflation)"
    
    items.append({
        "uid": "conversion",
        "title": conversion_text,
        "subtitle": f"Press Enter to copy conversion result",
        "arg": conversion_text,
        "valid": True,
        "icon": {
            "type": "default",
            "path": "icon.png"
        }
    })
    
    # Add individual purchasing power items (all items, no summary)
    if 'purchasing_power' in result and result['purchasing_power']:
        for item, quantity in result['purchasing_power'].items():
            if quantity >= 0.01:  # Only show items with reasonable quantities
                item_text = f"{quantity:.1f} {item}" if quantity >= 1 else f"{quantity:.2f} {item}"
                icon_path = get_icon_for_item(item)
                debug_log(f"Using icon '{icon_path}' for item '{item}'")
                items.append({
                    "uid": f"item_{item}",
                    "title": item_text,
                    "subtitle": f"Individual purchasing power for {item}",
                    "arg": f"{original} in {year} could buy {item_text}",
                    "valid": True,
                    "icon": {
                        "type": "default",
                        "path": icon_path
                    }
                })
    
    debug_log(f"Created {len(items)} Alfred items")
    return {"items": items}

def main():
    """Main entry point"""
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    
    debug_log(f"Alfred workflow started with query: '{query}'")
    debug_log(f"Working directory: {os.getcwd()}")
    debug_log(f"Script file: {__file__}")
    debug_log(f"Python executable: {sys.executable}")
    
    try:
        result = create_alfred_items(query)
        debug_log("Successfully created Alfred items")
        print(json.dumps(result, indent=2))
    except Exception as e:
        debug_log(f"Fatal error in main: {e}")
        debug_log(f"Exception type: {type(e).__name__}")
        import traceback
        debug_log(f"Traceback: {traceback.format_exc()}")
        
        # Fallback error response
        error_result = {
            "items": [{
                "uid": "fatal_error",
                "title": "Fatal Error",
                "subtitle": str(e),
                "arg": "",
                "valid": False,
                "icon": {
                    "type": "default",
                    "path": "icon.png"
                }
            }]
        }
        print(json.dumps(error_result, indent=2))

if __name__ == "__main__":
    main() 