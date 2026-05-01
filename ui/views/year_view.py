import customtkinter as ctk
from ui.widgets import style_button, build_year_nav_button
from functools import partial
from controllers import YearController, CalendarController
from constants import Direction
from ui.views.new_year_view import NewYearView

class YearView(ctk.CTkFrame):
    def __init__(self, parent, tracker_id, on_select, on_new_year, year):
        super().__init__(parent, width=400, height=300, corner_radius=15, border_width=4, border_color="black")

        self.controller = YearController()

        self.grid_propagate(False)

        self.parent = parent
        self.tracker_id = tracker_id
        self.on_select = on_select
        self.on_new_year = on_new_year
        self.year = year
        self.years = self.controller.get_years(tracker_id=self.tracker_id)
        self.build_ui()

    def build_months(self):
        self.months_dict = {}

        self.months = ctk.CTkFrame(self, fg_color="#2F2F2F")
        self.months.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.months.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.months.grid_rowconfigure((0, 1, 2), weight=1)

        for i in range(3):
            for j in range(4):
                num = (4*i) + j + 1
                button = style_button(
                    frame=self.months, 
                    text= num, 
                    command=partial(self.select, num), 
                    width=50,
                    height=50
                )
                button.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                self.months_dict[(i, j)] = button

    def next_year(self):
        if self.year + 1 not in self.years:
            self.new_year_popup(self.year+1)
        else:
            self.year += 1
            self.build_year()

    def prev_year(self):
        if self.year - 1 not in self.years:
            self.new_year_popup(self.year-1)
        else:
            self.year -= 1
            self.build_year()

    def update_year(self):
        self.year_label.configure(text=self.year)

    def add_year(self, year: int):
        controller = CalendarController()
        controller.add_year(tracker_id=self.tracker_id, year=year)

        self.on_new_year()

        # 1. Atualiza o estado local para o ano recém-criado
        self.year = year
        
        # 2. Atualiza a lista de anos disponíveis buscando do banco novamente
        self.years = self.controller.get_years(tracker_id=self.tracker_id)
        
        # 3. Reconstrói a barra superior para mostrar o novo ano
        self.build_year()

    def new_year_popup(self, year):
        self.popup_frame = NewYearView(self, on_save=partial(self.add_year, year), year=year)

        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.popup_frame.wait_visibility()
        self.popup_frame.grab_set()

    def build_year(self):
        if hasattr(self, "top_bar"):
            self.top_bar.destroy()

        self.top_bar = ctk.CTkFrame(self, fg_color="#2F2F2F")
        self.top_bar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.top_bar.grid_columnconfigure((0, 1, 2), weight=1)

        self.year_label = ctk.CTkLabel(self.top_bar, font=ctk.CTkFont(size=18), text=self.year)
        self.year_label.grid(row=0, column=1, sticky="we")

        self.btn_right = build_year_nav_button(self, self.top_bar, direction=Direction.NEXT, command=self.next_year)
        self.btn_right.grid(row=0, column=2, sticky="e")

        self.btn_left = build_year_nav_button(self, self.top_bar, direction=Direction.PREV, command=self.prev_year)
        self.btn_left.grid(row=0, column=0, sticky="w")

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1, uniform="main")
        #self.grid_columnconfigure(1, weight=4, uniform="main")
        self.grid_rowconfigure(0, weight=1, uniform="main")
        self.grid_rowconfigure(1, weight=3, uniform="main")

        self.build_months()
        self.build_year()

    def select(self, month: int):
        month_id = self.controller.get_month_id(tracker_id=self.tracker_id, year=self.year, month_number=month)
        self.on_select(month_id)
        self.destroy()