# config.py
backend_type = "redis"  # Change to "sqlite" for using SQLite

# Redis configuration
redis_config = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
}

# SQLite configuration
sqlite_config = {
    "database": "spamtrap_blocklist.db",
}

# Spamtrap addresses
spamtrap_addresses = [
    "spamtrap@example.com",
    # Add more spamtrap addresses as needed
]
