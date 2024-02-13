import redis
import sqlite3

class BlocklistBackend:
    def __init__(self, backend_type, config):
        self.backend_type = backend_type
        if backend_type == "redis":
            self.conn = redis.Redis(**config)
        elif backend_type == "sqlite":
            self.conn = sqlite3.connect(config['database'])
            self.init_sqlite()

    def init_sqlite(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS blocklist
                              (sender TEXT PRIMARY KEY NOT NULL);''')

    def add_blocked_sender(self, sender):
        if self.backend_type == "redis":
            key = f"SPAMTRAP|{sender}"
            self.conn.setex(key, 86400, 'blocked')  # 24 hours TTL
        elif self.backend_type == "sqlite":
            with self.conn:
                self.conn.execute("INSERT OR IGNORE INTO blocklist (sender) VALUES (?);", (sender,))

    def is_sender_blocked(self, sender):
        if self.backend_type == "redis":
            key = f"SPAMTRAP|{sender}"
            return self.conn.exists(key) > 0
        elif self.backend_type == "sqlite":
            cursor = self.conn.cursor()
            cursor.execute("SELECT sender FROM blocklist WHERE sender = ?;", (sender,))
            return cursor.fetchone() is not None
