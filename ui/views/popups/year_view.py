import customtkinter as ctk
from ui.widgets import CustomButton, NavigationButton
from functools import partial
from constants import Direction, MONTHS
from .new_year_view import NewYearView
from services import YearService, MonthService
from helper import format_month_text, format_year_text

class YearView(ctk.CTkFrame):
    def __init__(self, parent, tracker_id, on_select, year):
        super().__init__(
            parent, 
            width=500, 
            height=400,
            corner_radius=15,
            fg_color="#242424",
            border_width=1, 
            border_color="white"
        )

        self.year_service = YearService()
        self.month_service = MonthService()

        self.grid_propagate(False)

        self.parent = parent
        self.tracker_id = tracker_id
        self.on_select = on_select
        self.year: int = year
        self.years: list[int] = self.year_service.get_years_from_tracker(tracker_id=self.tracker_id)
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
                text = format_month_text(checked_days)
                button = CustomButton(self.months, 
                    text=f"{MONTHS[num]}\n{text}", 
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
        text = format_year_text(checked_days)
        self.year_info_label.configure(text=text)

        self.btn_right.update_button(self.year+1 not in self.years)
        self.btn_left.update_button(self.year-1 not in self.years)

        for btn in self.months_dict.values():
            checked_days = self.month_service.get_checked_days_count(self.tracker_id, self.year, btn.number)
            text = format_month_text(checked_days)
            btn.configure(text=f"{MONTHS[btn.number]}\n{text}")

    def add_year(self, year: int):
        self.year_service.add_tracker_year(tracker_id=self.tracker_id, year_number=year)

        self.year = year
        self.years = self.year_service.get_years_from_tracker(tracker_id=self.tracker_id)

        self.update_year()

    def new_year_popup(self, year):
        if hasattr(self, "popup_frame"):
            self.popup_frame.destroy()

        self.popup_frame = NewYearView(
            self.winfo_toplevel(), 
            on_save=partial(self.add_year, year), 
            year=year
        )

        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.popup_frame.wait_visibility()
        self.popup_frame.grab_set()

    def build_year(self):
        self.top_bar = ctk.CTkFrame(self.main_frame, fg_color="#252525", corner_radius=10)
        self.top_bar.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="ew")
        self.top_bar.grid_columnconfigure((0, 1, 2), weight=1)

        self.year_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent", corner_radius=10, height=55)
        self.year_frame.grid(row=0, column=1, pady=0, sticky="ew")
        self.year_frame.grid_columnconfigure(0, weight=1)

        self.year_label = ctk.CTkLabel(self.year_frame, font=ctk.CTkFont(size=20, weight="bold"), text=self.year, height=0)
        self.year_label.place(relx=0.5, rely=0.4, anchor="center")

        checked_days = self.year_service.get_checked_days_count(self.tracker_id, self.year)
        text = format_year_text(checked_days)

        self.year_info_label = ctk.CTkLabel(self.year_frame, font=ctk.CTkFont(size=15), text=text, height=0)
        self.year_info_label.place(relx=0.5, rely=0.75, anchor="center")

        self.btn_right = NavigationButton(
            parent=self.top_bar, 
            direction=Direction.NEXT, 
            command=self.next_year, 
            condition=self.year+1 not in self.years,
            height=40,
            width=40
        )
        self.btn_right.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        self.btn_left = NavigationButton(
            parent=self.top_bar, 
            direction=Direction.PREV, 
            command=self.prev_year, 
            condition=self.year-1 not in self.years,
            height=40,
            width=40
        )
        self.btn_left.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    def build_back_button(self):
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)

        self.back_button = CustomButton(self.button_frame, text="Voltar", command=self.destroy, font_size=15, height=35)
        self.back_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.build_months()
        self.build_year()
        self.build_back_button()

    def select(self, month: int):
        self.on_select(month, self.year)
        self.destroy()