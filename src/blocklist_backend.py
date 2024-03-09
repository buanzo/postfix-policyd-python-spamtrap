import redis
import sqlite3
import datetime

class BlocklistBackend:
    def __init__(self, backend_type, config):
        self.backend_type = backend_type
        if backend_type == "redis":
            self.conn = redis.Redis(**config)
        elif backend_type == "sqlite":
            self.conn = sqlite3.connect(config['database'])
            self.init_sqlite()
            self.upgrade_sqlite()  # Check and perform necessary upgrades

    def init_sqlite(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS blocklist
                              (sender TEXT PRIMARY KEY NOT NULL);''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS blocklist_timestamps
                              (sender TEXT PRIMARY KEY,
                               timestamp DATETIME NOT NULL,
                               FOREIGN KEY (sender) REFERENCES blocklist(sender));''')

    def upgrade_sqlite(self):
        # Assign a default timestamp to pre-existing entries without a timestamp
        default_timestamp = datetime.datetime.now() - datetime.timedelta(days=30)
        with self.conn as conn:
            # Identify senders in blocklist not in blocklist_timestamps
            senders_without_timestamp = conn.execute('''SELECT sender FROM blocklist 
                                                        WHERE sender NOT IN 
                                                        (SELECT sender FROM blocklist_timestamps);''').fetchall()
            # Insert a default timestamp for these senders
            conn.executemany('''INSERT INTO blocklist_timestamps (sender, timestamp) 
                                VALUES (?, ?);''', [(sender[0], default_timestamp) for sender in senders_without_timestamp])

    def add_blocked_sender(self, sender):
        if self.backend_type == "redis":
            key = f"SPAMTRAP|{sender}"
            # Set Redis key with a 3 months TTL (90 days * 24 hours * 60 minutes * 60 seconds)
            self.conn.setex(key, 90*24*60*60, 'blocked')
        elif self.backend_type == "sqlite":
            timestamp = datetime.datetime.now()
            with self.conn as conn:
                conn.execute("INSERT OR IGNORE INTO blocklist (sender) VALUES (?);", (sender,))
                conn.execute("INSERT OR REPLACE INTO blocklist_timestamps (sender, timestamp) VALUES (?, ?);",
                             (sender, timestamp))

    def is_sender_blocked(self, sender):
        if self.backend_type == "redis":
            key = f"SPAMTRAP|{sender}"
            return self.conn.exists(key) > 0
        elif self.backend_type == "sqlite":
            with self.conn as conn:
                result = conn.execute("SELECT sender FROM blocklist WHERE sender = ?;", (sender,)).fetchone()
                return result is not None
