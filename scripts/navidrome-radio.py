#!/usr/bin/env python3
"""
Navidrome Radio Station Manager
A CLI tool to search, browse, and add radio stations from Radio-Browser API
"""

import sqlite3
import requests
import json
import sys
from datetime import datetime
import hashlib
import base64
from typing import List, Dict, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================
RADIO_BROWSER_API = "https://de1.api.radio-browser.info/json"
CONFIG_FILE = None  # Set dynamically based on OS

# Global debug flag
DEBUG = False

# ============================================================================
# CONFIG FILE FUNCTIONS
# ============================================================================

def get_config_path() -> str:
    """Get the path to the config file based on OS"""
    import os
    if os.name == 'nt':  # Windows
        config_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'navidrome-radio')
    else:  # Linux/Mac
        config_dir = os.path.join(os.path.expanduser('~'), '.config', 'navidrome-radio')
    
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, 'config.json')

def load_config() -> Dict:
    """Load configuration from file"""
    config_path = get_config_path()
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error loading config: {e}")
    return {}

def save_config(config: Dict) -> bool:
    """Save configuration to file"""
    config_path = get_config_path()
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"[ERROR] Error saving config: {e}")
        return False

def get_db_path_from_config() -> Optional[str]:
    """Get database path from config file"""
    config = load_config()
    return config.get('db_path')

def set_db_path_in_config(db_path: str) -> bool:
    """Save database path to config file"""
    config = load_config()
    config['db_path'] = db_path
    return save_config(config)

def prompt_for_db_path() -> str:
    """Prompt user to enter database path on first run"""
    import os
    
    print("\n" + "="*70)
    print("[SETUP] FIRST-TIME SETUP: Database Path Required")
    print("="*70)
    print("\nThis tool needs to know the location of your Navidrome database.")
    print("\nCommon locations:")
    print("  Docker:  /path/to/navidrome/data/navidrome.db")
    print("  Linux:   /var/lib/navidrome/navidrome.db")
    print("  Windows: C:\\ProgramData\\Navidrome\\navidrome.db")
    print("\nTip: Check your docker-compose.yml or Navidrome config for the data path.")
    
    while True:
        db_path = input("\nEnter full path to navidrome.db: ").strip()
        
        if not db_path:
            print("[ERROR] Path cannot be empty!")
            continue
        
        # Expand user path (~)
        db_path = os.path.expanduser(db_path)
        
        if not os.path.exists(db_path):
            print(f"[ERROR] File not found: {db_path}")
            retry = input("Try again? (y/n): ").strip().lower()
            if retry != 'y':
                print("\n[ERROR] Cannot continue without a valid database path.")
                sys.exit(1)
            continue
        
        if not db_path.endswith('.db'):
            print("[WARNING] File doesn't end with .db - are you sure this is correct?")
            confirm = input("Use this path anyway? (y/n): ").strip().lower()
            if confirm != 'y':
                continue
        
        # Save to config
        if set_db_path_in_config(db_path):
            print(f"\n[OK] Database path saved to config!")
            print(f"   Config location: {get_config_path()}")
        
        return db_path

# Need os module for config functions
import os

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_id(name: str) -> str:
    """Generate a unique ID similar to Navidrome's format"""
    unique_string = f"{name}{datetime.utcnow().isoformat()}"
    hash_obj = hashlib.md5(unique_string.encode())
    return base64.b64encode(hash_obj.digest()).decode('utf-8').rstrip('=').replace('+', '-').replace('/', '_')[:22]

def get_timestamp() -> str:
    """Get current UTC timestamp in Navidrome format (matching web UI format)"""
    # Navidrome uses format: YYYY-MM-DD HH:MM:SS.microseconds (no timezone suffix)
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

def safe_print(message: str):
    """Print with fallback for terminals that don't support UTF-8/emojis"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Replace emojis with ASCII alternatives
        ascii_message = message.encode('ascii', 'replace').decode('ascii')
        print(ascii_message)

def debug_log(message: str):
    """Print debug message if DEBUG mode is enabled"""
    if DEBUG:
        print(f"[DEBUG] {message}")

def debug_log_dict(label: str, data: Dict):
    """Print a dictionary in debug mode"""
    if DEBUG:
        print(f"[DEBUG] {label}:")
        for key, value in data.items():
            print(f"  {key}: {repr(value)}")

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def check_station_exists(cursor, name: str, url: str) -> bool:
    """Check if a station already exists in the database"""
    debug_log(f"Checking if station exists: name='{name}', url='{url}'")
    cursor.execute("SELECT id FROM radio WHERE name = ? OR stream_url = ?", (name, url))
    result = cursor.fetchone()
    debug_log(f"Station exists check result: {result is not None}")
    return result is not None

def add_station_to_db(db_path: str, station: Dict) -> bool:
    """Add a single station to the database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        name = station['name']
        stream_url = station['url']
        home_page_url = station.get('homepage', '')
        
        debug_log_dict("Station data from API", station)
        
        if check_station_exists(cursor, name, stream_url):
            debug_log("Station already exists, skipping")
            conn.close()
            return False
        
        station_id = generate_id(name)
        timestamp = get_timestamp()
        
        debug_log(f"Generated ID: {station_id}")
        debug_log(f"Generated timestamp: {timestamp}")
        
        insert_values = {
            'id': station_id,
            'name': name,
            'stream_url': stream_url,
            'home_page_url': home_page_url,
            'created_at': timestamp,
            'updated_at': timestamp
        }
        debug_log_dict("Values to insert", insert_values)
        
        cursor.execute("""
            INSERT INTO radio (id, name, stream_url, home_page_url, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (station_id, name, stream_url, home_page_url, timestamp, timestamp))
        
        debug_log(f"INSERT executed, rows affected: {cursor.rowcount}")
        
        conn.commit()
        debug_log("Transaction committed")
        conn.close()
        return True
    except Exception as e:
        print(f"[ERROR] Error adding station: {e}")
        if DEBUG:
            import traceback
            traceback.print_exc()
        return False

def list_existing_stations(db_path: str):
    """List all existing stations in the database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, stream_url FROM radio ORDER BY name")
        stations = cursor.fetchall()
        conn.close()
        
        if not stations:
            print("\n[RADIO] No radio stations found in database.\n")
            return
        
        print("\n" + "="*80)
        print("[RADIO] CURRENT RADIO STATIONS IN NAVIDROME")
        print("="*80)
        for idx, (name, url) in enumerate(stations, 1):
            print(f"{idx:3d}. {name}")
            print(f"     URL: {url[:70]}{'...' if len(url) > 70 else ''}")
        print("="*80 + "\n")
    except Exception as e:
        print(f"[ERROR] Error reading database: {e}")

# ============================================================================
# DATABASE INSPECTION FUNCTIONS (for debugging)
# ============================================================================

def inspect_table_schema(db_path: str):
    """Display the complete schema of the radio table"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n" + "="*80)
        print("[SEARCH] RADIO TABLE SCHEMA")
        print("="*80)
        
        # Get table info
        cursor.execute("PRAGMA table_info(radio)")
        columns = cursor.fetchall()
        
        print(f"\n{'Column':<20} {'Type':<15} {'NotNull':<8} {'Default':<15} {'PK':<5}")
        print("-"*70)
        for col in columns:
            cid, name, col_type, notnull, default, pk = col
            print(f"{name:<20} {col_type:<15} {notnull:<8} {str(default):<15} {pk:<5}")
        
        # Get indexes
        print("\n[LIST] Indexes:")
        cursor.execute("PRAGMA index_list(radio)")
        indexes = cursor.fetchall()
        if indexes:
            for idx in indexes:
                print(f"  - {idx[1]} (unique: {idx[2]})")
        else:
            print("  No indexes found")
        
        # Get row count
        cursor.execute("SELECT COUNT(*) FROM radio")
        count = cursor.fetchone()[0]
        print(f"\n[STATS] Total stations in database: {count}")
        
        conn.close()
        print("="*80 + "\n")
    except Exception as e:
        print(f"[ERROR] Error inspecting schema: {e}")
        if DEBUG:
            import traceback
            traceback.print_exc()

def inspect_station_details(db_path: str, station_name: str = None):
    """Show full details of a station (all columns) for comparison"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute("PRAGMA table_info(radio)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if station_name:
            cursor.execute("SELECT * FROM radio WHERE name LIKE ?", (f"%{station_name}%",))
        else:
            # Get the most recent station
            cursor.execute("SELECT * FROM radio ORDER BY created_at DESC LIMIT 1")
        
        station = cursor.fetchone()
        conn.close()
        
        if not station:
            print("\n[ERROR] No matching station found.\n")
            return
        
        print("\n" + "="*80)
        print("[SEARCH] STATION DETAILS (ALL COLUMNS)")
        print("="*80)
        
        for col_name, value in zip(columns, station):
            # Truncate long values for display
            str_value = str(value) if value is not None else "NULL"
            if len(str_value) > 60:
                str_value = str_value[:60] + "..."
            print(f"{col_name:<20}: {str_value}")
        
        print("="*80 + "\n")
    except Exception as e:
        print(f"[ERROR] Error inspecting station: {e}")
        if DEBUG:
            import traceback
            traceback.print_exc()

def compare_stations(db_path: str):
    """Compare two stations side by side to identify differences"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute("PRAGMA table_info(radio)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Get all stations
        cursor.execute("SELECT name FROM radio ORDER BY name")
        stations = cursor.fetchall()
        conn.close()
        
        if len(stations) < 2:
            print("\n[ERROR] Need at least 2 stations to compare.\n")
            return
        
        print("\n" + "="*80)
        print("[LIST] SELECT STATIONS TO COMPARE")
        print("="*80)
        for idx, (name,) in enumerate(stations, 1):
            print(f"{idx:3d}. {name}")
        
        try:
            choice1 = int(input("\nSelect first station number: ").strip())
            choice2 = int(input("Select second station number: ").strip())
            
            if not (1 <= choice1 <= len(stations) and 1 <= choice2 <= len(stations)):
                print("[ERROR] Invalid selection!")
                return
            
            name1 = stations[choice1 - 1][0]
            name2 = stations[choice2 - 1][0]
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM radio WHERE name = ?", (name1,))
            station1 = cursor.fetchone()
            
            cursor.execute("SELECT * FROM radio WHERE name = ?", (name2,))
            station2 = cursor.fetchone()
            
            conn.close()
            
            print("\n" + "="*80)
            print("[SEARCH] STATION COMPARISON")
            print("="*80)
            print(f"\n{'Column':<20} | {'Station 1':<30} | {'Station 2':<30}")
            print("-"*85)
            
            for idx, col_name in enumerate(columns):
                val1 = str(station1[idx]) if station1[idx] is not None else "NULL"
                val2 = str(station2[idx]) if station2[idx] is not None else "NULL"
                
                # Truncate
                val1_display = val1[:28] + ".." if len(val1) > 30 else val1
                val2_display = val2[:28] + ".." if len(val2) > 30 else val2
                
                # Mark differences
                marker = "[!]" if val1 != val2 else "  "
                print(f"{col_name:<20} | {val1_display:<30} | {val2_display:<30} {marker}")
            
            print("="*80)
            print("[!]  = Values differ between stations")
            print("="*80 + "\n")
            
        except ValueError:
            print("[ERROR] Please enter valid numbers!")
    except Exception as e:
        print(f"[ERROR] Error comparing stations: {e}")
        if DEBUG:
            import traceback
            traceback.print_exc()

def inspect_menu(db_path: str):
    """Database inspection menu for debugging"""
    while True:
        print_header()
        print("[SEARCH] DATABASE INSPECTION (Debug)\n")
        print("1. View radio table schema")
        print("2. View latest station details (all columns)")
        print("3. Search and view station details")
        print("4. Compare two stations side by side")
        print("5. Back to main menu")
        
        choice = get_user_choice("Select option", range(1, 6))
        
        if choice == "1":
            print_header()
            inspect_table_schema(db_path)
            input("\nPress Enter to continue...")
        
        elif choice == "2":
            print_header()
            inspect_station_details(db_path)
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            name = input("\nEnter station name to search: ").strip()
            if name:
                print_header()
                inspect_station_details(db_path, name)
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            print_header()
            compare_stations(db_path)
            input("\nPress Enter to continue...")
        
        elif choice == "5":
            return

# ============================================================================
# RADIO BROWSER API FUNCTIONS
# ============================================================================

def search_stations(query: str, search_type: str = "byname") -> List[Dict]:
    """
    Search for stations on Radio-Browser
    search_type: byname, bytag, bycountry, bylanguage, bystate
    """
    try:
        url = f"{RADIO_BROWSER_API}/stations/{search_type}/{query}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] Error searching Radio-Browser: {e}")
        return []

def get_top_stations(limit: int = 50) -> List[Dict]:
    """Get top voted stations"""
    try:
        url = f"{RADIO_BROWSER_API}/stations/topvote/{limit}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] Error fetching top stations: {e}")
        return []

def get_stations_by_tag(tag: str) -> List[Dict]:
    """Get stations by tag/genre"""
    return search_stations(tag, "bytag")

def get_stations_by_country(country: str) -> List[Dict]:
    """Get stations by country"""
    return search_stations(country, "bycountry")

# ============================================================================
# UI FUNCTIONS
# ============================================================================

def clear_screen():
    """Clear the terminal screen"""
    import os
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header():
    """Print application header"""
    clear_screen()
    print("\n" + "="*80)
    print("***  NAVIDROME RADIO STATION MANAGER  ***")
    print("="*80 + "\n")

def display_stations(stations: List[Dict], selected: set = None):
    """Display a list of stations with optional selection markers"""
    if not stations:
        print("No stations found.")
        return
    
    selected = selected or set()
    
    print("\n" + "-"*80)
    for idx, station in enumerate(stations, 1):
        marker = "x" if idx in selected else " "
        name = station.get('name', 'Unknown')
        country = station.get('country', 'Unknown')
        tags = station.get('tags', '')
        bitrate = station.get('bitrate', 'N/A')
        votes = station.get('votes', 0)
        
        print(f"[{marker}] {idx:3d}. {name[:50]:<50}")
        print(f"         Country: {country:<15} Tags: {tags[:30]}")
        print(f"         Bitrate: {bitrate} kbps | Votes: {votes}")
        print(f"         URL: {station.get('url', '')[:70]}")
        print("-"*80)

def display_page_stations(stations: List[Dict], start_idx: int, selected: set = None):
    """Display a page of stations with global indexing"""
    if not stations:
        print("No stations found.")
        return
    
    selected = selected or set()
    
    print("\n" + "-"*80)
    for page_idx, station in enumerate(stations, 1):
        global_idx = start_idx + page_idx  # Global index
        marker = "x" if global_idx in selected else " "
        name = station.get('name', 'Unknown')
        country = station.get('country', 'Unknown')
        tags = station.get('tags', '')
        bitrate = station.get('bitrate', 'N/A')
        votes = station.get('votes', 0)
        
        print(f"[{marker}] {global_idx:3d}. {name[:50]:<50} (Page #{page_idx})")
        print(f"         Country: {country:<15} Tags: {tags[:30]}")
        print(f"         Bitrate: {bitrate} kbps | Votes: {votes}")
        print(f"         URL: {station.get('url', '')[:70]}")
        print("-"*80)

def get_user_choice(prompt: str, valid_range: Optional[range] = None) -> str:
    """Get user input with optional validation"""
    while True:
        choice = input(f"\n{prompt}: ").strip()
        if not valid_range:
            return choice
        
        if choice.isdigit() and int(choice) in valid_range:
            return choice
        
        print(f"[ERROR] Please enter a number between {valid_range.start} and {valid_range.stop - 1}")

# ============================================================================
# MAIN MENU FUNCTIONS
# ============================================================================

def search_menu(db_path: str):
    """Search and select stations"""
    print_header()
    print("[SEARCH] SEARCH RADIO STATIONS\n")
    print("1. Search by name")
    print("2. Search by genre/tag")
    print("3. Search by country")
    print("4. Browse top voted stations")
    print("5. Back to main menu")
    
    choice = get_user_choice("Select option", range(1, 6))
    
    stations = []
    
    if choice == "1":
        query = input("\nEnter station name: ").strip()
        if query:
            print(f"\n[SEARCH] Searching for '{query}'...")
            stations = search_stations(query, "byname")
    
    elif choice == "2":
        query = input("\nEnter genre/tag (e.g., jazz, rock, classical): ").strip()
        if query:
            print(f"\n[SEARCH] Searching for genre '{query}'...")
            stations = get_stations_by_tag(query)
    
    elif choice == "3":
        query = input("\nEnter country (e.g., USA, UK, Germany): ").strip()
        if query:
            print(f"\n[SEARCH] Searching for country '{query}'...")
            stations = get_stations_by_country(query)
    
    elif choice == "4":
        print("\n[SEARCH] Fetching top voted stations...")
        stations = get_top_stations(50)
    
    elif choice == "5":
        return
    
    if not stations:
        print("\n[ERROR] No stations found!")
        input("\nPress Enter to continue...")
        return
    
    print(f"\n[OK] Found {len(stations)} stations!")
    input("\nPress Enter to browse results...")
    select_and_add_stations(stations, db_path)

def select_and_add_stations(stations: List[Dict], db_path: str):
    """Allow user to select multiple stations and add them with pagination"""
    selected = set()
    page = 0
    items_per_page = 10
    total_pages = (len(stations) - 1) // items_per_page + 1
    
    while True:
        print_header()
        
        # Calculate pagination
        start_idx = page * items_per_page
        end_idx = min(start_idx + items_per_page, len(stations))
        page_stations = stations[start_idx:end_idx]
        
        print(f"[RADIO] FOUND {len(stations)} STATIONS - SELECT TO ADD")
        print(f"Page {page + 1} of {total_pages} (Showing {start_idx + 1}-{end_idx} of {len(stations)})")
        print(f"Selected: {len(selected)} station(s)\n")
        
        # Display current page with global indexing
        display_page_stations(page_stations, start_idx, selected)
        
        print("\nCommands:")
        print("  [number]     - Toggle selection (global number)")
        print("  [n1-n2]      - Select range on current page")
        print("  n/next       - Next page")
        print("  p/prev       - Previous page")
        print("  page [n]     - Go to specific page")
        print("  all          - Select all on current page")
        print("  none         - Deselect all")
        print("  add          - Add selected stations to Navidrome")
        print("  back         - Back to search menu")
        
        choice = input("\nEnter command: ").strip().lower()
        
        if choice == "back":
            return
        
        elif choice in ["n", "next"]:
            if page < total_pages - 1:
                page += 1
            else:
                print("[ERROR] Already on last page!")
                input("Press Enter to continue...")
        
        elif choice in ["p", "prev"]:
            if page > 0:
                page -= 1
            else:
                print("[ERROR] Already on first page!")
                input("Press Enter to continue...")
        
        elif choice.startswith("page "):
            try:
                target_page = int(choice.split()[1]) - 1
                if 0 <= target_page < total_pages:
                    page = target_page
                else:
                    print(f"[ERROR] Page must be between 1 and {total_pages}")
                    input("Press Enter to continue...")
            except:
                print("[ERROR] Invalid page number!")
                input("Press Enter to continue...")
        
        elif choice == "all":
            # Select all on current page
            for i in range(start_idx + 1, end_idx + 1):
                selected.add(i)
        
        elif choice == "none":
            selected.clear()
        
        elif choice == "add":
            if not selected:
                print("\n[ERROR] No stations selected!")
                input("\nPress Enter to continue...")
                continue
            
            add_selected_stations(stations, selected, db_path)
            return
        
        elif "-" in choice:
            try:
                start, end = choice.split("-")
                start, end = int(start.strip()), int(end.strip())
                # Adjust to current page
                if 1 <= start <= items_per_page and 1 <= end <= items_per_page:
                    global_start = start_idx + start
                    global_end = start_idx + end
                    if global_end <= end_idx:
                        selected.update(range(global_start, global_end + 1))
                    else:
                        print("[ERROR] Range exceeds current page!")
                        input("Press Enter to continue...")
                else:
                    print(f"[ERROR] Range must be between 1 and {min(items_per_page, len(page_stations))} for current page")
                    input("Press Enter to continue...")
            except:
                print("[ERROR] Invalid range format! Use: 1-5")
                input("Press Enter to continue...")
        
        elif choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(stations):
                if num in selected:
                    selected.remove(num)
                else:
                    selected.add(num)
            else:
                print(f"[ERROR] Please enter a number between 1 and {len(stations)}")
                input("Press Enter to continue...")

def add_selected_stations(stations: List[Dict], selected: set, db_path: str):
    """Add the selected stations to the database"""
    print_header()
    print(f"[SAVE] ADDING {len(selected)} STATIONS TO NAVIDROME\n")
    
    added = 0
    skipped = 0
    
    for idx in sorted(selected):
        station = stations[idx - 1]
        name = station.get('name', 'Unknown')
        
        if add_station_to_db(db_path, station):
            print(f"[OK] Added: {name}")
            added += 1
        else:
            print(f"[SKIP]  Skipped (already exists): {name}")
            skipped += 1
    
    print(f"\n{'='*80}")
    print(f"[STATS] SUMMARY: {added} added, {skipped} skipped")
    print(f"{'='*80}")
    print("\n[TIP] Refresh your Navidrome web interface to see the new stations!")
    input("\nPress Enter to continue...")

def main_menu(db_path: str):
    """Main application menu"""
    while True:
        print_header()
        if DEBUG:
            print("[DEBUG MODE ENABLED]\n")
        # Show current database path
        print(f"[DB] Database: {db_path}\n")
        print("MAIN MENU\n")
        print("1. Search and add radio stations")
        print("2. View existing stations in database")
        print("3. Inspect database (debug)")
        print("4. Change database path")
        print("5. Exit")
        
        choice = get_user_choice("Select option", range(1, 6))
        
        if choice == "1":
            search_menu(db_path)
        
        elif choice == "2":
            print_header()
            list_existing_stations(db_path)
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            inspect_menu(db_path)
        
        elif choice == "4":
            print_header()
            new_path = prompt_for_db_path()
            if new_path and os.path.exists(new_path):
                db_path = new_path
                print("\n[OK] Database path updated!")
            input("\nPress Enter to continue...")
        
        elif choice == "5":
            print("\n Thanks for using Navidrome Radio Station Manager!\n")
            sys.exit(0)

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main application entry point"""
    global DEBUG
    db_path = None
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    # Check for help
    if '-h' in args or '--help' in args:
        saved_path = get_db_path_from_config()
        print("\nNavidrome Radio Station Manager")
        print("="*50)
        print("\nUsage:")
        print("  navidrome-radio                    - Use saved/configured database path")
        print("  navidrome-radio <db_path>          - Use custom database path")
        print("  navidrome-radio --debug            - Enable verbose debug logging")
        print("  navidrome-radio --debug <db_path>  - Debug mode with custom path")
        print("  navidrome-radio --reset-config     - Reset saved configuration")
        print("\nOptions:")
        print("  -h, --help       Show this help message")
        print("  --debug          Enable verbose debug output (shows SQL, IDs, etc.)")
        print("  --reset-config   Clear saved database path and re-prompt")
        print(f"\nConfig file location:")
        print(f"  {get_config_path()}")
        if saved_path:
            print(f"\nCurrently configured database path:")
            print(f"  {saved_path}")
        else:
            print(f"\nNo database path configured (will prompt on first run)")
        print("\nDebug mode will show:")
        print("  - Exact values being inserted into the database")
        print("  - Generated IDs and timestamps")
        print("  - SQL execution details")
        print("  - Full stack traces on errors")
        print()
        sys.exit(0)
    
    # Check for reset-config flag
    if '--reset-config' in args:
        args.remove('--reset-config')
        config_path = get_config_path()
        if os.path.exists(config_path):
            os.remove(config_path)
            safe_print("\n[OK] Configuration reset. You will be prompted for the database path.\n")
        else:
            safe_print("\n[INFO] No configuration file found.\n")
        if not args:  # If only --reset-config was passed, continue to prompt
            pass
    
    # Check for debug flag
    if '--debug' in args:
        DEBUG = True
        args.remove('--debug')
        safe_print("\n[DEBUG] Debug mode enabled - verbose logging active\n")
    
    # Determine database path (priority: CLI arg > saved config > prompt)
    if args:
        # Path provided via command line
        db_path = args[0]
        debug_log(f"Using CLI-provided database path: {db_path}")
    else:
        # Try to load from config
        db_path = get_db_path_from_config()
        if db_path:
            debug_log(f"Using saved database path: {db_path}")
            safe_print(f"\nUsing saved database path: {db_path}")
            safe_print(f"   (Use --reset-config to change)\n")
        else:
            # First run - prompt for path
            db_path = prompt_for_db_path()
    
    # Verify database exists
    if not os.path.exists(db_path):
        print(f"\n[ERROR] Database not found at: {db_path}")
        print("\nOptions:")
        print(f"  1. Run with --reset-config to set a new path")
        print(f"  2. Provide path directly: {sys.argv[0]} /path/to/navidrome.db\n")
        sys.exit(1)
    
    # Start the application
    try:
        main_menu(db_path)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}\n")
        if DEBUG:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
