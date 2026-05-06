from sqlalchemy.orm import Session
from repositories import YearRepository
from dtos import YearDTO
# from dtos import YearDTO # Descomente quando criar o DTO do Ano

class YearService:
    def __init__(self, db: Session):
        self.db = db
        self.year_repository = YearRepository(self.db)

    def get_year_by_id(self, year_id: int) -> YearDTO | None:
        year = self.year_repository.get_year_by_id(year_id)
        if not year:
            return None
        return YearDTO.from_entity(year)

    def get_year_by_number(self, tracker_id: int, year_number: int) -> YearDTO | None:
        year = self.year_repository.get_specific_year(tracker_id, year_number)
        if not year:
            return None
        return YearDTO.from_entity(year)

    def get_years_from_tracker(self, tracker_id: int) -> list[int]:
        """
        Como o seu YearController e a interface esperam uma lista de números [2024, 2025, 2026],
        já retornamos apenas os inteiros aqui.
        """
        years = self.year_repository.get_years_from_tracker(tracker_id)
        if not years:
            return []
        return [y.number for y in years]

    def add_tracker_year(self, tracker_id: int, year_number: int) -> YearDTO | None:
        """
        Tenta criar o ano. Retorna True se sucesso, False se o ano já existia.
        """
        MIN_YEAR = 2000
        MAX_YEAR = 2100
        
        if not (MIN_YEAR <= year_number <= MAX_YEAR):
            return False # Evita criar o ano 9999 sem querer na interface

        created_year = self.year_repository.create_year_with_cascade(tracker_id, year_number)
        if not created_year:
            return None
        return YearDTO.from_entity(created_year)
    
    def delete_year(self, tracker_id: int, year_number: int) -> bool:
        return self.year_repository.delete_year(tracker_id, year_number)
            