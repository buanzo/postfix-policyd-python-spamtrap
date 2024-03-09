#!/usr/bin/env python3
import sqlite3
import datetime
from config import sqlite_config  # Import the configuration from config.py

def delete_old_entries(db_path, months=3):
    """Delete entries older than the specified number of months."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Calculate the cutoff date
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=30*months)
    
    # Delete old entries from blocklist_timestamps
    cursor.execute("DELETE FROM blocklist_timestamps WHERE timestamp < ?", (cutoff_date,))
    
    # Delete orphaned entries from blocklist
    cursor.execute("DELETE FROM blocklist WHERE sender NOT IN (SELECT sender FROM blocklist_timestamps)")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Use the database path from the sqlite_config imported from config.py
    delete_old_entries(sqlite_config['database'])
