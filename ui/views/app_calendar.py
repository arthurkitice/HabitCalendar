import customtkinter as ctk
from functools import partial
from dtos import DayDTO
from ui.views.new_year_view import NewYearView
from ui.views.year_view import YearView
from config import get_last_month, get_last_year, save_current_date
from ui.widgets import NavigationButton, DayButton, style_button
from constants import Direction, MONTHS, WEEK_DAYS
from controllers import CalendarController
import calendar

CALENDAR_ROWS = 6
CALENDAR_COLS = 7

class MainCalendarView(ctk.CTkFrame):
    def __init__(self, parent, initial_tracker_id, controller: CalendarController):
        super().__init__(parent, fg_color="transparent") 
        self.controller = controller
        
        self.current_tracker_id = initial_tracker_id
        self.current_month = get_last_month(self.current_tracker_id)
        self.current_year = get_last_year(self.current_tracker_id)
        self.years = self.controller.get_years(tracker_id=self.current_tracker_id)
        
        self.day_buttons: list[DayButton] = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.build_ui()

    def update_tracker_data(self, tracker_id: int):
        """Chamado pela Sidebar quando o marcador muda"""
        self.current_tracker_id = tracker_id
        self.current_month = get_last_month(self.current_tracker_id)
        self.current_year = get_last_year(self.current_tracker_id)
        self.years = self.controller.get_years(tracker_id=self.current_tracker_id)
        
        # Proteção contra anos deletados
        if self.years and self.current_year not in self.years:
            self.current_year = self.years[0]
            self.current_month = 1
            save_current_date(self.current_tracker_id, self.current_month, self.current_year)

        self.update_top_bar()
        self.update_days_frame()

    # ================================
    # MÉTODOS DE INTERAÇÃO COM O BANCO
    # ================================
    def check_day(self, index: int) -> None:
        self.day_buttons[index].check_day()
        self.controller.check_day(
            tracker_id=self.current_tracker_id, 
            year=self.current_year,
            month=self.current_month,
            day = self.day_buttons[index].day
        )

    def add_year(self, year: int) -> None:
        self.controller.add_year(tracker_id=self.current_tracker_id, year=year)
        self._refresh_years()
        
        self.current_year = year
        self.current_month = 12 if year < self.current_year else 1
        
        save_current_date(self.current_tracker_id, self.current_month, self.current_year)
        self.update_top_bar()
        self.update_days_frame()

    def _refresh_years(self):
        """Atualiza apenas a lista de anos disponíveis para o popup e botões de navegação"""
        self.years = self.controller.get_years(tracker_id=self.current_tracker_id)

    # =======================
    # MÉTODOS DOS DIAS DO MÊS
    # =======================
    def style_empty_buttons(self) -> None:
        first_week_day, month_days = calendar.monthrange(self.current_year, self.current_month)
        first_week_day = (first_week_day+1)%7

        prev_year = self.current_year - 1 if self.current_month == 1 else self.current_year
        prev_month = 12 if self.current_month == 1 else self.current_month - 1
        last_month_days = calendar.monthrange(prev_year, prev_month)[1]

        prev_days = range(last_month_days - first_week_day + 1, last_month_days + 1)
        next_days = range(1, 42 - month_days - first_week_day + 1)
        
        filler_number = list(prev_days) + list(next_days)
        empty_indexes = [i for i, btn in enumerate(self.day_buttons) if btn.day == "0"]
        
        for index, number in zip(empty_indexes, filler_number):
            self.day_buttons[index].update_button(day=number, command=None, checked=False, disabled=True)

    def previous_month(self) -> None:
        if self.current_month == 1:
            if self.current_year - 1 not in self.years:
                self.open_new_year_popup(self.current_year-1)
                return
            self.current_year -= 1
        self.current_month = (self.current_month-2)%12 + 1
        self.update_calendar()

    def next_month(self) -> None:
        if self.current_month == 12:
            if self.current_year + 1 not in self.years:
                self.open_new_year_popup(self.current_year+1)
                return
            self.current_year += 1
        self.current_month = (self.current_month%12)+1
        self.update_calendar()

    def update_calendar(self):
        save_current_date(self.current_tracker_id, self.current_month, self.current_year)
        self.update_top_bar()
        self.update_days_frame()

    def jump_to_month(self, target_month: int, target_year: int) -> None:
        """Chamado pelo popup de visualização de anos. Limpo e sem queries desnecessárias."""
        self.current_month = target_month
        self.current_year = target_year
        self.update_calendar()
    
    def _generate_month_cells(self) -> list[DayDTO]:
        month_days = self.controller.get_specific_days(
            tracker_id=self.current_tracker_id, 
            year=self.current_year, 
            month=self.current_month
        )
        
        first_week_day = (calendar.monthrange(self.current_year, self.current_month)[0] + 1) % 7
        empty_day: DayDTO = DayDTO(id=0, number=0, checked=False, month_id=0)

        total_cells = CALENDAR_ROWS * CALENDAR_COLS
        all_cells: list[DayDTO] = [empty_day] * first_week_day + month_days
        all_cells.extend([empty_day] * (total_cells - len(all_cells)))

        return all_cells
    
    def update_days_frame(self) -> None:
        for i, (btn, day) in enumerate(zip(self.day_buttons, self._generate_month_cells())):
            btn.update_button(day=day.number, checked=day.checked, command=partial(self.check_day, i))
        
        self.style_empty_buttons()

    def build_days_frame(self) -> None:
        self.days_frame = ctk.CTkFrame(self, corner_radius=10)
        self.days_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.days_frame.grid_columnconfigure(tuple(range(CALENDAR_COLS)), weight=1, uniform="days")
        self.days_frame.grid_rowconfigure(tuple(range(CALENDAR_ROWS)), weight=1, uniform="days")
        
        all_cells = self._generate_month_cells()
        self.day_buttons.clear()

        for index, day in enumerate(all_cells):
            row, col = divmod(index, CALENDAR_COLS)
            button = DayButton(
                self.days_frame, 
                day=day.number, 
                checked=day.checked, 
                command=partial(self.check_day, index)
            )
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.day_buttons.append(button)
        
        self.style_empty_buttons()
    
    def open_new_year_popup(self, year: int) -> None:
        if getattr(self, "popup_frame", None) and self.popup_frame.winfo_exists():
            self.popup_frame.destroy()

        self.popup_frame = NewYearView(self, on_save=partial(self.add_year, year), year=year)
        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.popup_frame.wait_visibility()
        self.popup_frame.grab_set()

    # ===============================
    # TOP BAR (NAVEGAÇÃO ENTRE MESES)
    # ===============================
    def open_years_popup(self, year: int):
        if getattr(self, "popup_frame", None) and self.popup_frame.winfo_exists():
            self.popup_frame.destroy()
        
        self.popup_frame = YearView(
            parent=self.winfo_toplevel(), 
            tracker_id=self.current_tracker_id, 
            on_select=self.jump_to_month,
            year=year
        )
        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.popup_frame.wait_visibility()
        self.popup_frame.grab_set()

    def update_top_bar(self) -> None:
        month_text = MONTHS[self.current_month]
        self.month_button.configure(
            text=f"{self.current_year}\n{month_text}", 
            command=partial(self.open_years_popup, self.current_year)
        )

        self.prev_button.update_button(condition=self._get_condition(Direction.PREV))
        self.next_button.update_button(condition=self._get_condition(Direction.NEXT))

    def build_top_bar(self) -> None:
        self.top_frame = ctk.CTkFrame(self, corner_radius=10)
        self.top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.top_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="main")
        self.top_frame.grid_rowconfigure(0 , weight=1)

        month_text = MONTHS[self.current_month]

        self.month_button = style_button(
            parent=self.top_frame,
            text=f"{self.current_year}\n{month_text}",
            command=partial(self.open_years_popup, self.current_year),
            font=ctk.CTkFont(size=20, weight="bold"), 
            fg_color="transparent",
        )
        self.month_button.grid(row=0, column=1, padx=5, pady=5)

        self.prev_button = NavigationButton(
            parent=self.top_frame, 
            direction=Direction.PREV, 
            command=partial(self.previous_month),
            condition=self._get_condition(Direction.PREV)
        )
        self.prev_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.next_button = NavigationButton(
            parent=self.top_frame, 
            direction=Direction.NEXT, 
            command=partial(self.next_month),
            condition=self._get_condition(Direction.NEXT)
        )
        self.next_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    def build_week_days_frame(self) -> None:
        self.week_days_frame = ctk.CTkFrame(self, corner_radius=10)
        self.week_days_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew")
        self.week_days_frame.grid_columnconfigure(tuple(range(CALENDAR_COLS)), weight=1, uniform="week_days")
        self.week_days_frame.grid_rowconfigure(0, weight=1)

        for i, day in enumerate(WEEK_DAYS):
            label = ctk.CTkLabel(self.week_days_frame, text=day, font=ctk.CTkFont(size=15, weight="bold"), text_color="white")
            label.grid(row=0, column=i, padx=5, pady=5)

    def _get_condition(self, direction: Direction) -> bool | None:
        match direction:
            case Direction.NEXT:
                return self.current_year +1 not in self.years and self.current_month == 12
            case Direction.PREV:
                return self.current_year -1 not in self.years and self.current_month == 1
            case _:
                return None
            
    def build_ui(self) -> None:
        self.build_top_bar()
        self.build_week_days_frame()
        self.build_days_frame()