import customtkinter as ctk
from repositories import DayRepository, MonthRepository
from dtos import DayDTO
from database import get_db
from helper import get_reversed_days
from config import get_last_month_index, save_current_month_index
from ui.widgets import (
    build_day_button, 
    build_navigation_button, 
    update_day_button, 
    update_navigation_button, 
    update_empty_button
)

class CalendarApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calendário")
        self.geometry("1100x700")

        self.minsize(500, 350)

        self.months = self.get_months()
        self.current_month_index = get_last_month_index()
        self.btn_dict = {}
        self.build_ui()

    def get_months(self):
        try:
            with get_db() as db:
                month_repository = MonthRepository(db)
                months = month_repository.get_all_months()
                return months
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def get_days(self, month_number):
        try:
            with get_db() as db:
                month_repository = MonthRepository(db)
                days = month_repository.get_days_by_month_number(month_number)
                return days
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def check_day(self, day_id, row, column):
        try:
            with get_db() as db:
                day_repository = DayRepository(db)
                day = day_repository.check_day(day_id)
                update_day_button(self, self.btn_dict[(row, column)], day, (row, column))
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def change_month(self, opperation):
        if opperation == "next":
            if self.current_month_index + 1 < len(self.months):
                self.current_month_index += 1
            
        elif opperation == "prev":
            if self.current_month_index - 1 >= 0:
                self.current_month_index -= 1

        save_current_month_index(self.current_month_index)

        self.update_top_bar()
        self.update_days_frame()
    
    def style_empty_buttons(self):
        cont=0
        for btn in self.btn_dict.values():
            if btn.cget("text") != " ":
                break
            cont+=1
        prev_month_days = get_reversed_days(self.months[self.current_month_index - 1].number if self.current_month_index > 0 else 12) 
        filler_number = 0
        for btn in self.btn_dict.values():
            if cont > 0:
                day = prev_month_days[cont-1]
                update_empty_button(self, btn, DayDTO(id=0, number=day, checked=False, month_id=0))
                cont -= 1

            elif btn.cget("text") == " ":
                filler_number += 1
                update_empty_button(self, btn, DayDTO(id=0, number=filler_number, checked=False, month_id=0))
        
    def build_button(self, day, row, column):
        button = build_day_button(self, day, row, column)
        button.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

        return button

    def update_days_frame(self):
        days = self.get_days(self.months[self.current_month_index].number)
        filler_number = 0

        for key, btn in self.btn_dict.items():
            if days:
                day = days.pop(0)
            else:
                day = DayDTO(id=0, number=filler_number, checked=False, month_id=0)

            update_day_button(self, btn, day, key, clickable=day.number != 0)
        
        self.style_empty_buttons()

    def build_days_frame(self):
        days = self.get_days(self.months[self.current_month_index].number)
        filler_number = 0
        for i in range(6):
            for j in range(7):
                if days :
                    day = days.pop(0)
                else:
                    day = DayDTO(id=0, number=filler_number, checked=False, month_id=0)

                self.btn_dict[(i, j)] = self.build_button(day, i, j)

        self.style_empty_buttons()

    def update_top_bar(self):
        self.month_label.configure(text=self.months[self.current_month_index].name, text_color="white")

        update_navigation_button(self, self.prev_button, "prev", disabled=self.current_month_index == 0)

        update_navigation_button(self, self.next_button, "next", disabled=self.current_month_index >= len(self.months) - 1)

    def build_top_bar(self):
        self.month_label = ctk.CTkLabel(
            self.top_frame, 
            text=self.months[self.current_month_index].name, 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        self.month_label.grid(row=0, column=1, padx=5, pady=5)

        self.prev_button = build_navigation_button(self, "prev")
        self.prev_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.next_button = build_navigation_button(self, "next")
        self.next_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    def build_week_days_frame(self):
        week_days = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        for i, day in enumerate(week_days):
            label = ctk.CTkLabel(self.week_days_frame, text=day, font=ctk.CTkFont(size=15, weight="bold"), text_color="white")
            label.grid(row=0, column=i, padx=5, pady=5)

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.top_frame = ctk.CTkFrame(self, corner_radius=0)
        self.top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.top_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="main")
        self.top_frame.grid_rowconfigure(0 , weight=1)

        self.days_frame = ctk.CTkFrame(self, corner_radius=0)
        self.days_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.days_frame.grid_columnconfigure(tuple(range(7)), weight=1, uniform="days")
        self.days_frame.grid_rowconfigure(tuple(range(6)), weight=1, uniform="days")

        self.week_days_frame = ctk.CTkFrame(self, corner_radius=0)
        self.week_days_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew")
        self.week_days_frame.grid_columnconfigure(tuple(range(7)), weight=1, uniform="week_days")
        self.week_days_frame.grid_rowconfigure(0, weight=1)

        self.build_top_bar()
        self.build_days_frame()
        self.build_week_days_frame()