import sqlite3
from models import Month, MonthWithDays

class MonthRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_all_months(self):
        rows = self.conn.execute("SELECT * FROM months").fetchall()
        return [Month.from_row(row) for row in rows] if rows else None

    def get_month_by_id(self, month_id: int):
        row = self.conn.execute("SELECT * FROM months WHERE id = ?", (month_id,)).fetchone()
        return Month.from_row(row) if row else None
    
    def get_month_with_days_by_id(self, month_id: int):
        month_row = self.conn.execute("SELECT * FROM months WHERE id = ?", (month_id,)).fetchone()
        day_row = self.conn.execute("SELECT * FROM days WHERE month_id = ?", (month_id,)).fetchall()

        return MonthWithDays.from_rows(month_row, day_row) if month_row and day_row else None
    
    def get_month_by_year_number(self, tracker_id: int, year: int, month_number: int):
        
        sql = """
            SELECT m.* FROM months AS m
            JOIN years AS y ON m.year_id = y.id
            WHERE y.tracker_id = ? AND y.number = ? AND m.number = ?
        """

        row = self.conn.execute(sql, (tracker_id, year, month_number)).fetchone()

        return Month.from_row(row) if row else None
    
    def get_all_checked_days(self, tracker_id: int, year: int, month: int) -> int:
        """Retorna a quantidade de dias marcados no mês"""

        sql = """
            SELECT SUM(d.checked) FROM days AS d
            JOIN months AS m ON d.month_id = m.id
            JOIN years AS y ON m.year_id = y.id
            WHERE y.tracker_id = ? AND y.number = ? AND m.number = ?
        """

        result = self.conn.execute(sql, (tracker_id, year, month)).fetchone()

        return result[0] if result[0] is not None else 0