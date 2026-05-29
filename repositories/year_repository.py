import calendar
from models import Year, Month
import sqlite3

class YearRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_year_by_id(self, year_id: int) -> Year | None:
        row = self.conn.execute("SELECT * FROM years WHERE id = ?", (year_id,)).fetchone()
        return Year.from_row(row) if row else None

    def get_years_from_tracker(self, tracker_id: int):
        rows = self.conn.execute("SELECT * FROM years WHERE tracker_id = ? ORDER BY number ASC", (tracker_id,)).fetchall()
        return [Year.from_row(row) for row in rows]

    def get_specific_year(self, tracker_id: int, year_number: int) -> Year | None:
        row = self.conn.execute("SELECT * FROM years WHERE tracker_id = ? AND number = ?", (tracker_id, year_number)).fetchone()
        return Year.from_row(row) if row else None

    def create_year_with_cascade(self, tracker_id: int, year_number: int) -> Year | None:
        if self.get_specific_year(tracker_id, year_number):
            return None 

        new_year_id = self.conn.execute("INSERT INTO years (number, tracker_id) VALUES (?, ?)", (year_number, tracker_id)).lastrowid

        for month_number in range(1, 13):
            month_id = self.conn.execute("INSERT INTO months (number, year_id) VALUES (?, ?)", (month_number, new_year_id)).lastrowid
            
            days_in_month = calendar.monthrange(year_number, month_number)[1]
            for day_number in range(1, days_in_month + 1):
                self.conn.execute("INSERT INTO days (number, month_id) VALUES (?, ?)", (day_number, month_id))
        
        return self.get_year_by_id(new_year_id)
    
    def delete_year(self, tracker_id: int, year_number: int) -> bool:
        cursor = self.conn.execute("DELETE FROM years WHERE number = ? AND tracker_id = ?", (year_number, tracker_id))
        return cursor.rowcount > 0 #Se deletou algo incrementa o rowcount
    
    def get_all_checked_days(self, tracker_id: int, year: int) -> int:
        """Retorna a quantidade de dias marcados"""

        if self.get_year_by_id(tracker_id) is None:
            return 0
        
        sql = """
            SELECT SUM(d.checked) FROM days AS d
            JOIN months AS m ON d.month_id = m.id
            JOIN years AS y ON m.year_id = y.id
            WHERE y.tracker_id = ? AND y.number = ?
        """

        result = self.conn.execute(sql, (tracker_id, year)).fetchone()

        return result[0] if result[0] is not None else 0