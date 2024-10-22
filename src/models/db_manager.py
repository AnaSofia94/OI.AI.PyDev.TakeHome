import sqlite3

class DatabaseManager:
    def __init__(self, db_file: str = 'video_metadata.db'):
        self.db_file = db_file
        self._initialize_db()

    def _initialize_db(self):
        """Initialize the video metadata table in the SQLite database."""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS video_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_file TEXT UNIQUE,  -- Enforce unique file names to avoid duplicates
                compressed_file TEXT,
                original_size REAL,
                compressed_size REAL,
                compression_ratio REAL
            )
        ''')
        conn.commit()
        conn.close()

    def log_metadata(self, original_file, compressed_file, original_size, compressed_size):
        """Log the metadata of a compressed video into the database."""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        compression_ratio = compressed_size / original_size
        c.execute('''
            INSERT OR IGNORE INTO video_metadata (original_file, compressed_file, original_size, compressed_size, compression_ratio)
            VALUES (?, ?, ?, ?, ?)
        ''', (original_file, compressed_file, original_size, compressed_size, compression_ratio))
        conn.commit()
        conn.close()

    def fetch_all_metadata(self):
        """Fetch all video metadata from the database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM video_metadata")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def find_video_by_filename(self, original_file):
        """Check if a video with the given filename already exists in the database."""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM video_metadata WHERE original_file = ?", (original_file,))
        row = c.fetchone()
        conn.close()
        return row