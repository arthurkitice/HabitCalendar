from database import get_connection

def create_tables():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trackers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS years (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER NOT NULL,
                tracker_id INTEGER,
                FOREIGN KEY (tracker_id) REFERENCES trackers (id) ON DELETE CASCADE,
                UNIQUE (number, tracker_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS months (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER NOT NULL,
                year_id INTEGER,
                FOREIGN KEY (year_id) REFERENCES years (id) ON DELETE CASCADE,
                UNIQUE (number, year_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER NOT NULL,
                checked INTEGER DEFAULT 0,
                month_id INTEGER,
                FOREIGN KEY (month_id) REFERENCES months (id) ON DELETE CASCADE,
                UNIQUE (number, month_id)
            )
        """)