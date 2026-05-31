from models import Tracker, Month, Day, Year
from datetime import datetime
import sqlite3

class TrackerRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_tracker_by_id(self, tracker_id: int) -> Tracker | None:
        row = self.conn.execute("SELECT * FROM trackers WHERE id = ?", (tracker_id,)).fetchone()
        return Tracker.from_row(row) if row else None

    def get_tracker_by_name(self, tracker_name: str) -> Tracker | None:
        row = self.conn.execute("SELECT * FROM trackers WHERE name = ?", (tracker_name,)).fetchone()
        return Tracker.from_row(row) if row else None
    
    def get_all_trackers(self) -> list[Tracker]:
        rows = self.conn.execute("SELECT * FROM trackers").fetchall()
        return [Tracker.from_row(row) for row in rows]

    def create_tracker(self, name: str) -> Tracker | None:
        if self.get_tracker_by_name(name):
            return None
        
        self.conn.execute("INSERT INTO trackers (name) VALUES (?)", (name,))

        return self.get_tracker_by_name(name)

    def update_tracker(self, tracker_id: int, name: str) -> Tracker | None:
        if self.get_tracker_by_id(tracker_id) is None:
            return None
        
        self.conn.execute("UPDATE trackers SET name = ? WHERE id = ?", (name, tracker_id))
        new_tracker = self.get_tracker_by_name(name)

        return new_tracker

    def delete_tracker(self, tracker_id: int) -> bool:
        if self.get_tracker_by_id(tracker_id) is None:
            return False
            
        self.conn.execute("DELETE FROM trackers WHERE id = ?", (tracker_id,))
        return True
    
    def get_all_checked_days(self, tracker_id: int) -> int:
        """Retorna a quantidade de dias marcados totais do tracker"""

        if self.get_tracker_by_id(tracker_id) is None:
            return 0
        
        sql = """
            SELECT SUM(d.checked) FROM days AS d
            JOIN months AS m ON d.month_id = m.id
            JOIN years AS y ON m.year_id = y.id
            WHERE y.tracker_id = ?
        """

        result = self.conn.execute(sql, (tracker_id,)).fetchone()

        return result[0] if result[0] is not None else 0