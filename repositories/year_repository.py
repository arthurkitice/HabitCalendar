import calendar
from sqlalchemy.orm import Session
from models import Year, Month, Day
from constants import MONTHS

class YearRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_year_by_id(self, year_id: int) -> Year | None:
        return self.db.query(Year).filter(Year.id == year_id).first()

    def get_years_from_tracker(self, tracker_id: int):
        """Retorna todos os anos de um marcador, ordenados"""
        return self.db.query(Year).filter(Year.tracker_id == tracker_id).order_by(Year.number.asc()).all()

    def get_specific_year(self, tracker_id: int, year_number: int) -> Year | None:
        return self.db.query(Year).filter(Year.tracker_id == tracker_id, Year.number == year_number).first()

    def create_year_with_cascade(self, tracker_id: int, year_number: int) -> Year | None:
        """
        Gera o Ano, seus 12 Meses e todos os Dias automaticamente.
        """
        # Proteção: Evita duplicar um ano que já existe
        if self.get_specific_year(tracker_id, year_number):
            return False 

        new_year = Year(number=year_number, tracker_id=tracker_id)
        self.db.add(new_year)
        self.db.flush() # Pega o ID do ano gerado

        for month_number in range(1, 13):
            new_month = Month(name=MONTHS[month_number], number=month_number, year_id=new_year.id)
            self.db.add(new_month)
            self.db.flush() # Pega o ID do mês gerado

            # Verifica quantos dias o mês tem naquele ano específico (bissextos inclusos)
            days_in_month = calendar.monthrange(year_number, month_number)[1]
            
            for day_number in range(1, days_in_month + 1):
                new_day = Day(number=day_number, checked=False, month_id=new_month.id)
                self.db.add(new_day)

        # Se não deu erro em nenhum dia de nenhum mês, salva tudo de uma vez
        self.db.commit()
        self.db.refresh(new_year)
        
        return new_year
    
    def delete_year(self, tracker_id: int, year_number: int) -> bool:
        year = self.get_specific_year(tracker_id, year_number)
        if not year:
            return False

        self.db.delete(year)
        self.db.commit()
        return True