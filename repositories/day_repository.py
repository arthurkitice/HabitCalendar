import sqlite3
from models.day import Day

class DayRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_day_by_id(self, day_id: int) -> Day | None:
        sql = "SELECT * FROM days WHERE id = ?"
        row = self.conn.execute(sql, (day_id,)).fetchone()
        return Day.from_row(row) if row else None
    
    def get_day_number(self, day_id: int) -> int | None:
        sql = "SELECT number FROM days WHERE id = ?"
        row = self.conn.execute(sql, (day_id,)).fetchone()
        return row["number"] if row else None

    def check_day(self, day_id: int):
        sql = "UPDATE days SET checked = NOT checked WHERE id = ?"
        self.conn.execute(sql, (day_id,))
    
    def get_specific_day(self, tracker_id: int, year: int, month: int, day: int) -> Day | None:
        """Retorna um dia específico em um mês, ano e tracker, sem precisar do ID's do dia, mês e ano"""
        
        sql = """
            SELECT d.* FROM days AS d
            JOIN months AS m ON d.month_id = m.id
            JOIN years AS y ON m.year_id = y.id
            WHERE d.number = ? 
              AND m.number = ? 
              AND y.number = ? 
              AND y.tracker_id = ?
        """
        
        row = self.conn.execute(sql, (day, month, year, tracker_id)).fetchone()
        
        return Day.from_row(row) if row else None