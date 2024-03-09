#!/usr/bin/env python3
import sqlite3
import datetime
from config import sqlite_config  # Import the configuration from config.py
import argparse

def delete_old_entries(db_path, months=3, verbose=False):
    """Delete entries older than the specified number of months."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Calculate the cutoff date
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=30*months)
    
    if verbose:
        # If verbose, print the senders to be deleted
        cursor.execute("SELECT sender FROM blocklist_timestamps WHERE timestamp < ?", (cutoff_date,))
        for row in cursor.fetchall():
            print(f"Deleting: {row[0]}")
    
    # Delete old entries from blocklist_timestamps
    cursor.execute("DELETE FROM blocklist_timestamps WHERE timestamp < ?", (cutoff_date,))
    
    # Delete orphaned entries from blocklist
    cursor.execute("DELETE FROM blocklist WHERE sender NOT IN (SELECT sender FROM blocklist_timestamps)")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Maintenance script for blocklist cleanup.')
    parser.add_argument('--verbose', action='store_true', help='List deleted entries')
    args = parser.parse_args()

    # Use the database path from the sqlite_config imported from config.py
    delete_old_entries(sqlite_config['database'], verbose=args.verbose)
