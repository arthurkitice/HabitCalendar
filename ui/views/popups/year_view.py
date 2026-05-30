import customtkinter as ctk
from ui.widgets import CustomButton, NavigationButton, PopupFrame
from functools import partial
from themes import SECONDARY_THEME
from services import YearService, MonthService
from config import ThemeJSON
from icon_assets import RIGHT_ARROW, LEFT_ARROW
import i18n

class YearView(PopupFrame):
    def __init__(self, parent, tracker_id, on_select, year, on_new_year):
        super().__init__(parent)

        self.year_service = YearService()
        self.month_service = MonthService()

        self.parent = parent
        self.tracker_id = tracker_id
        self.on_select = on_select
        self.year: int = year
        self.years: list[int] = self.year_service.get_years_from_tracker(tracker_id=self.tracker_id)
        self.on_new_year = on_new_year
        self.build_ui()

    def build_months(self):
        self.months_dict = {}

        self.months = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.months.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        self.months.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.months.grid_rowconfigure((0, 1, 2), weight=1)

        for i in range(3):
            for j in range(4):
                num = (4*i) + j + 1
                checked_days = self.month_service.get_checked_days_count(self.tracker_id, self.year, num)
                month = i18n.t(f'calendar.months.{str(num)}')
                checks = i18n.t(f'checks', count=checked_days) if checked_days > 0 else ""
                button = CustomButton(self.months, 
                    text=f"{month}\n{checks}", 
                    command=partial(self.select, num), 
                    font=ctk.CTkFont(size=13), 
                    main_color=False,
                    width=100, 
                    height=75
                )
                button.number = num
                button.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                self.months_dict[(i, j)] = button

    def next_year(self):
        if self.year + 1 not in self.years:
            self.new_year_popup(self.year+1)
        else:
            self.year += 1
            self.update_year()

    def prev_year(self):
        if self.year - 1 not in self.years:
            self.new_year_popup(self.year-1)
        else:
            self.year -= 1
            self.update_year()

    def update_year(self):
        self.year_label.configure(text=self.year)

        checked_days = self.year_service.get_checked_days_count(self.tracker_id, self.year)
        checks = i18n.t(f'checks', count=checked_days)
        self.year_info_label.configure(text=checks)

        self.btn_right.update_button(self.year+1 not in self.years)
        self.btn_left.update_button(self.year-1 not in self.years)

        for btn in self.months_dict.values():
            checked_days = self.month_service.get_checked_days_count(self.tracker_id, self.year, btn.number)
            month = i18n.t(f'calendar.months.{str(btn.number)}')
            checks = i18n.t(f'checks', count=checked_days) if checked_days > 0 else ""
            btn.configure(text=f"{month}\n{checks}")

    def add_year(self, year: int):
        self.year_service.add_tracker_year(tracker_id=self.tracker_id, year_number=year)
        self.year = year
        self.years = self.year_service.get_years_from_tracker(tracker_id=self.tracker_id)
        self.on_new_year()
        self.update_year()

    def new_year_popup(self, year):
        if ThemeJSON.is_new_year_popup_hidden():
            self.add_year(year)
            return

        from . import PopupHandler
        self.popup_frame = PopupHandler.new_year_popup(
            self, 
            on_save=partial(self.add_year, year), 
            year=year
        )

    def build_year(self):
        self.top_bar = ctk.CTkFrame(self.main_frame, fg_color=SECONDARY_THEME.fg_color(), corner_radius=10)
        self.top_bar.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="ew")
        self.top_bar.grid_columnconfigure((0, 1, 2), weight=1)

        self.year_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent", corner_radius=10, height=50)
        self.year_frame.grid(row=0, column=1, pady=0, sticky="ew")
        self.year_frame.grid_columnconfigure(0, weight=1)

        self.year_label = ctk.CTkLabel(self.year_frame, font=ctk.CTkFont(size=20, weight="bold"), text=self.year, height=0)
        self.year_label.place(relx=0.5, rely=0.4, anchor="center")

        checked_days = self.year_service.get_checked_days_count(self.tracker_id, self.year)
        checks = i18n.t(f'checks', count=checked_days)

        self.year_info_label = ctk.CTkLabel(self.year_frame, font=ctk.CTkFont(size=15), text=checks, height=0)
        self.year_info_label.place(relx=0.5, rely=0.75, anchor="center")

        self.btn_right = NavigationButton(
            parent=self.top_bar, 
            icon=RIGHT_ARROW, 
            command=self.next_year, 
            condition=self.year+1 not in self.years,
            height=40,
            width=40
        )
        self.btn_right.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        self.btn_left = NavigationButton(
            parent=self.top_bar, 
            icon=LEFT_ARROW, 
            command=self.prev_year, 
            condition=self.year-1 not in self.years,
            height=40,
            width=40
        )
        self.btn_left.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    def build_ui(self):
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.build_months()
        self.build_year()
        self.build_back_button()

    def select(self, month: int):
        self.on_select(month, self.year)
        self.destroy()