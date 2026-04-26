import customtkinter as ctk
from functools import partial
from services import TrackerService, MonthService, DayService
from dtos import DayDTO
from ui.views.new_tracker_view import AlterTrackerFrame
from ui.views.new_year_view import NewYearView
from database import get_db
from helper import get_days, get_reversed_days
from config import get_last_month_index, save_current_month_index
from ui.widgets import (
    build_day_button, 
    build_navigation_button, 
    update_day_button, 
    update_navigation_button, 
    update_empty_button,
    build_sidebar_button,
    build_sidebar_edit_button,
    build_sidebar_remove_button,
    style_button
)

CALENDAR_ROWS = 6
CALENDAR_COLS = 7
SIDEBAR_WEIGHT = 1
MAIN_WEIGHT = 4

class CalendarApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calendário")
        self.geometry("1100x700")

        self.minsize(500, 350)

        self.sidebar_visible = True

        trackers = self.get_trackers()

        self.current_tracker_id = trackers[0].id if trackers else 0

        self.months = self.get_months()

        if not self.months:
            self.months = []

        self.current_month_index = get_last_month_index()
        
        # 4. Proteção: garante que o índice do JSON não é maior que a lista de meses
        if self.months and self.current_month_index >= len(self.months):
            self.current_month_index = 0

        self.new_tracker_window = None
        self.btn_dict = {}
        
        self.normal_content =  True if self.get_trackers() else False

        self.build_ui()

    # ================================
    # MÉTODOS DE INTERAÇÃO COM O BANCO
    # ================================

    def get_months(self):
        try:
            with get_db() as db:
                tracker_service = TrackerService(db)
                trackers_with_months = tracker_service.get_tracker_with_months_by_id(self.current_tracker_id)
                months = trackers_with_months.months if trackers_with_months else None
                return months
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def get_days(self, month_id):
        try:
            with get_db() as db:
                month_service = MonthService(db)
                month = month_service.get_month_with_days_by_id(month_id)
                return month.days
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def get_trackers(self):
        try:
            with get_db() as db:
                tracker_service = TrackerService(db)
                trackers = tracker_service.get_all_trackers()
                return trackers
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def get_tracker_by_id(self, tracker_id):
        try:
            with get_db() as db:
                tracker_service = TrackerService(db)
                tracker = tracker_service.get_tracker_by_id(tracker_id)
                return tracker
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def check_day(self, day_id, row, column):
        try:
            with get_db() as db:
                day_service = DayService(db)
                day = day_service.check_day(day_id)
                update_day_button(self, self.btn_dict[(row, column)], day, (row, column))
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def add_year(self, year):
        try:
            with get_db() as db:
                tracker_service = TrackerService(db)

                current_month_id = self.months[self.current_month_index].id
                current_year = self.months[self.current_month_index].year

                tracker_service.add_tracker_year(tracker_id=self.current_tracker_id, year=year)

                self.months = self.get_months()

                for i, month in enumerate(self.months):
                    if month.id == current_month_id:
                        self.current_month_index = i

                operation = "prev" if year < current_year else "next"

                self.change_month(operation)
        except Exception as e:
            print(f"Erro inesperado: {e}")

    # =======================
    # MÉTODOS DOS DIAS DO MÊS
    # =======================

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

    def change_month(self, operation):
        first_month = self.current_month_index - 1 < 0 and operation == "prev"
        last_month = self.current_month_index + 1 >= len(self.months) and operation == "next"

        if  first_month or last_month:
            self.open_new_year_popup(1 if last_month else -1)
            return

        if operation == "next":
            self.current_month_index += 1
            
        elif operation == "prev":
            self.current_month_index -= 1

        save_current_month_index(self.current_month_index)

        self.update_top_bar()
        self.update_days_frame()

    # ====================
    # FRAME DE DIAS DO MẼS
    # ====================

    def update_days_frame(self):
        if not self.months:
            return
        current_month = self.months[self.current_month_index]

        days = self.get_days(current_month.id)
        week_days = get_days(current_month.year, current_month.number)

        for key, btn in self.btn_dict.items():
            if len(week_days) == 0 or week_days.pop(0) == 0:
                day = DayDTO(id=0, number=0, checked=False, month_id=0)
            else:
                day = days.pop(0)

            update_day_button(self, btn, day, key, clickable=day.number != 0)
        
        self.style_empty_buttons()

    def build_days_frame(self):
        if self.months:
            current_month = self.months[self.current_month_index]
            days = self.get_days(current_month.id)
            week_days = get_days(current_month.year, current_month.number)
            for i in range(CALENDAR_ROWS):
                for j in range(CALENDAR_COLS):
                    if len(week_days) == 0 or week_days.pop(0) == 0:
                        day = DayDTO(id=0, number=0, checked=False, month_id=0)
                    else:
                        day = days.pop(0)

                    self.btn_dict[(i, j)] = self.build_button(day, i, j)

            self.style_empty_buttons()
        else:
            for i in range(CALENDAR_ROWS):
                for j in range(CALENDAR_COLS):
                    day = DayDTO(id=0, number=0, checked=False, month_id=0)
                    self.btn_dict[(i, j)] = self.build_button(day, i, j)
    
    def open_new_year_popup(self, operation):

        if operation not in [-1, 1]:
            print(f"Operação inválida: {operation}")
            return
        
        if getattr(self, "popup_frame", None) and self.popup_frame.winfo_exists():
            self.popup_frame.destroy()
        
        current_year = self.months[self.current_month_index].year

        year = current_year + operation

        self.popup_frame = NewYearView(self, on_save=partial(self.add_year, year), year=year)
    
        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.popup_frame.wait_visibility()
        self.popup_frame.grab_set()

    # ===============================
    # TOP BAR (NAVEGAÇÃO ENTRE MESES)
    # ===============================

    def update_top_bar(self):
        if not self.months:
            return
        
        current_month = self.months[self.current_month_index]

        self.month_label.configure(text=f"{current_month.year}\n{current_month.name}", text_color="white")

        update_navigation_button(self, self.prev_button, "prev")

        update_navigation_button(self, self.next_button, "next")

    def build_top_bar(self):
        
        
        if not self.months:
            year, name = None, None
        else: 
            current_month = self.months[self.current_month_index]
            year, name = current_month.year, current_month.name
        self.month_label = ctk.CTkLabel(
            self.top_frame, 
            text=f"{year}\n{name}", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        self.month_label.grid(row=0, column=1, padx=5, pady=5)

        self.prev_button = build_navigation_button(self, direction="prev", command=partial(self.change_month, "prev"))
        self.prev_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.next_button = build_navigation_button(self, direction="next", command=partial(self.change_month, "next"))
        self.next_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    # ========================
    # FRAME DE DIAS DA SEMANA
    # ========================

    def build_week_days_frame(self):
        week_days = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        for i, day in enumerate(week_days):
            label = ctk.CTkLabel(self.week_days_frame, text=day, font=ctk.CTkFont(size=15, weight="bold"), text_color="white")
            label.grid(row=0, column=i, padx=5, pady=5)

    # ==================
    # MÉTODOS DA SIDEBAR
    # ==================

    def edit_tracker(self, name, tracker_id):
        try:
            with get_db() as db:
                tracker_service = TrackerService(db)
                tracker_service.update_tracker(tracker_id, name)
                self.build_sidebar_buttons()
                self.update_sidebar()
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def remove_tracker(self, tracker_id):
        try:
            with get_db() as db:
                tracker_service = TrackerService(db)
                tracker_service.delete_tracker(tracker_id)

                trackers = self.get_trackers()
                last_tracker_id = trackers[-1].id if trackers else 0

                # Atualiza os componentes e troca para o último tracker criado caso o
                # tracker selecionado seja removido ou não existam trackers
                if last_tracker_id == 0 or tracker_id == self.current_tracker_id:
                    self.change_tracker(last_tracker_id)
                    self.update_components()

                self.build_sidebar_buttons()
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def open_new_tracker_popup(self, operation, tracker=None):

        if operation not in ["create", "edit"]:
            print(f"Operação inválida: {operation}")
            return
        
        if getattr(self, "popup_frame", None) and self.popup_frame.winfo_exists():
            self.popup_frame.destroy()
        
        if operation == "create":
            self.popup_frame = AlterTrackerFrame(self, on_save=self.create_new_tracker)
        else:
            self.popup_frame = AlterTrackerFrame(
                self, 
                on_save=self.edit_tracker, 
                tracker_id=tracker.id, 
                tracker_name=tracker.name
            )
        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.popup_frame.wait_visibility()
        self.popup_frame.grab_set()

    def change_tracker(self, tracker_id):
        self.current_tracker_id = tracker_id
        self.update_components()

    def create_new_tracker(self, tracker_name):
        try:
            with get_db() as db:
                tracker_service = TrackerService(db)
                tracker_service.create_tracker(name=tracker_name)
                self.build_sidebar_buttons()
        except Exception as e:
            print(f"Erro inesperado: {e}")

        if self.current_tracker_id == 0:
            trackers = self.get_trackers()
            self.current_tracker_id = trackers[0].id if trackers else 0
            self.update_components()

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.grid_forget()
            # Passar string vazia no uniform para quebrar a união da coluna com as outras
            # Assim o customtkinter consegue expremer o conteúdo dela isolado no canto
            # Se passar o mesmo nome das outras o ctk entende que mesmo que seja weight 0 
            # ainda faz parte da união e não expreme todo o conteúdo
            self.reduced_sidebar_frame.grid(row=0, column=0, rowspan=4, padx=(0, 5), pady=20, sticky="nsew")
            self.grid_columnconfigure(0, weight=0, uniform="")

        else:
            self.reduced_sidebar_frame.grid_forget()
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, padx=(0, 20), pady=20, sticky="nsew")
            self.grid_columnconfigure(0, weight=1, uniform="window")

        self.sidebar_visible = not self.sidebar_visible

    # =====================
    # SIDEBAR DE MARCADORES
    # =====================

    def build_sidebar_buttons(self):
        trackers = self.get_trackers()
        self.tracker_btn = {}

        if getattr(self, "sidebar_buttons_frame", None):
            self.sidebar_buttons_frame.destroy()

        self.sidebar_buttons_frame = ctk.CTkFrame(self.sidebar_frame, corner_radius=0)
        self.sidebar_buttons_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.sidebar_buttons_frame.grid_columnconfigure(0, weight=1)

        if not trackers:
            return

        for i, tracker in enumerate(trackers):
            self.tracker_btn[tracker.id] = build_sidebar_button(self, tracker.name, command=partial(self.change_tracker, tracker.id))
            self.tracker_btn[tracker.id].grid(row=i+1, column=0, padx=10, pady=10, sticky="we")

            edit_btn = build_sidebar_edit_button(self, command=partial(self.open_new_tracker_popup, "edit", tracker))
            edit_btn.grid(row=i+1, column=1, padx=5, pady=10, sticky="we")

            remove_btn = build_sidebar_remove_button(self, command=partial(self.remove_tracker, tracker.id))
            remove_btn.grid(row=i+1, column=2, padx=5, pady=10, sticky="we")

    def update_sidebar(self):
        tracker = self.get_tracker_by_id(self.current_tracker_id)
        tracker_text = tracker.name if tracker is not None else "Nenhum"
        self.tracker_label.configure(text=f"Marcador atual:\n{tracker_text}", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")

    def build_sidebar(self):
        self.sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="Marcadores", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        self.sidebar_label.grid(row=0, column=0, padx=5, pady=5)

        self.add_tracker_button = style_button(self.sidebar_frame, text="+", command=partial(self.open_new_tracker_popup, "create"), width=50)
        self.add_tracker_button.grid(row=0, column=1, padx=5, pady=5)

        self.hide_sidebar_button = style_button(self.sidebar_frame, text="<", command=self.toggle_sidebar, width=50)
        self.hide_sidebar_button.grid(row=0, column=2, padx=5, pady=5, sticky = "w")

        tracker = self.get_tracker_by_id(self.current_tracker_id)
        tracker_text = tracker.name if tracker is not None else "Nenhum"

        self.tracker_frame = ctk.CTkFrame(self.sidebar_frame, corner_radius=0)
        self.tracker_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.tracker_frame.grid_columnconfigure(0, weight=1)

        self.tracker_label = ctk.CTkLabel(self.tracker_frame, text=f"Marcador atual:\n{tracker_text}", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        self.tracker_label.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")

        self.build_sidebar_buttons()
    
    def build_reduced_sidebar(self):
        self.toggle_button = style_button(self.reduced_sidebar_frame, text=">", command=self.toggle_sidebar, width=40)
        self.toggle_button.grid(row=0, column=0, padx=0, pady=5, sticky="w")

    # ===============
    # FORBIDDEN FRAME
    # ===============

    def forbidden_check(self):
        if self.get_trackers() and not self.normal_content:
            self.normal_content = True
            self.show_normal_content()
        elif not self.get_trackers() and self.normal_content:
            self.normal_content = False
            self.show_forbidden_content()

    def show_forbidden_content(self):
        self.top_frame.grid_forget()
        self.days_frame.grid_forget()
        self.week_days_frame.grid_forget()
        self.forbidden_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=0)
    
    def show_normal_content(self):
        self.forbidden_frame.grid_forget()
        self.top_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        self.days_frame.grid(row=2, column=1, padx=20, pady=(0, 20), sticky="nsew")
        self.week_days_frame.grid(row=1, column=1, padx=20, pady=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.update_components()
        
    def build_forbidden_content(self):
        self.forbidden_label = ctk.CTkLabel(
            self.forbidden_frame, 
            text="Adicione um novo marcador\nclicando no botão '+' da barra lateral\npara visualizar algum calendário",
            font=ctk.CTkFont(size=20),
            text_color="gray"
        )
        self.forbidden_label.grid(row=0, column=0, sticky="nsew")

    def update_components(self):
        self.months = self.get_months()
        if not self.months:
            self.months = []

        self.update_days_frame()
        self.update_sidebar()
        self.update_top_bar()
        self.forbidden_check()

    # =======================
    # CONSTRUÇÃO DA INTERFACE
    # =======================

    def build_ui(self):
        self.top_frame = ctk.CTkFrame(self, corner_radius=0)
        self.top_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        self.top_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="main")
        self.top_frame.grid_rowconfigure(0 , weight=1)

        self.days_frame = ctk.CTkFrame(self, corner_radius=0)
        self.days_frame.grid(row=2, column=1, padx=20, pady=(0, 20), sticky="nsew")
        self.days_frame.grid_columnconfigure(tuple(range(CALENDAR_COLS)), weight=1, uniform="days")
        self.days_frame.grid_rowconfigure(tuple(range(CALENDAR_ROWS)), weight=1, uniform="days")

        self.week_days_frame = ctk.CTkFrame(self, corner_radius=0)
        self.week_days_frame.grid(row=1, column=1, padx=20, pady=0, sticky="nsew")
        self.week_days_frame.grid_columnconfigure(tuple(range(CALENDAR_COLS)), weight=1, uniform="week_days")
        self.week_days_frame.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, padx=(0, 20), pady=20, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        self.reduced_sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.reduced_sidebar_frame.grid_columnconfigure(0, weight=1)

        self.forbidden_frame = ctk.CTkFrame(self, corner_radius=0)
        self.forbidden_frame.grid_columnconfigure(0, weight=1)
        self.forbidden_frame.grid_rowconfigure(0, weight=1)
        self.build_forbidden_content()

        self.grid_columnconfigure(0, weight=SIDEBAR_WEIGHT, uniform="window")
        self.grid_columnconfigure(1, weight=MAIN_WEIGHT, uniform="window")
        self.grid_rowconfigure(2, weight=1)

        self.build_top_bar()
        self.build_days_frame()
        self.build_week_days_frame()
        self.build_sidebar()
        self.build_reduced_sidebar()

        self.forbidden_check()