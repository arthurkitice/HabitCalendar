import customtkinter as ctk
from repositories import DayRepository, MonthRepository, TrackerRepository
from dtos import DayDTO
from ui.views.new_tracker_view import AlterTrackerWindow
from database import get_db
from helper import get_reversed_days
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

class CalendarApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calendário")
        self.geometry("1100x700")

        self.minsize(500, 350)

        self.sidebar_visible = True

        trackers = self.get_trackers()

        self.current_tracker_id = trackers[0].id if trackers else 1

        self.months = self.get_months()

        if not self.months:
            self.months = []

        self.current_month_index = get_last_month_index()
        
        # 4. Proteção: garante que o índice do JSON não é maior que a lista de meses
        if self.months and self.current_month_index >= len(self.months):
            self.current_month_index = 0

        self.new_tracker_window = None
        self.btn_dict = {}
        
        # Só constrói a UI se tiver meses carregados
        if self.months:
            self.build_ui()
        else:
            print("Nenhum mês ou tracker encontrado no banco de dados!")

    # ================================
    # MÉTODOS DE INTERAÇÃO COM O BANCO
    # ================================

    def get_months(self):
        try:
            with get_db() as db:
                tracker_repository = TrackerRepository(db)
                months = tracker_repository.get_tracker_with_months_by_id(self.current_tracker_id).months
                return months
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def get_days(self, month_id):
        try:
            with get_db() as db:
                month_repository = MonthRepository(db)
                # Chama a função baseada no ID, e não no número!
                days = month_repository.get_days_by_month_id(month_id) 
                return days
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def get_trackers(self):
        try:
            with get_db() as db:
                tracker_repository = TrackerRepository(db)
                trackers = tracker_repository.get_all_trackers()
                return trackers
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def get_tracker_by_id(self, tracker_id):
        try:
            with get_db() as db:
                tracker_repository = TrackerRepository(db)
                tracker = tracker_repository.get_dto_tracker_by_id(tracker_id)
                return tracker
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

    # ====================
    # FRAME DE DIAS DO MẼS
    # ====================

    def update_days_frame(self):
        days = self.get_days(self.months[self.current_month_index].id)
        filler_number = 0

        for key, btn in self.btn_dict.items():
            if days:
                day = days.pop(0)
            else:
                day = DayDTO(id=0, number=filler_number, checked=False, month_id=0)

            update_day_button(self, btn, day, key, clickable=day.number != 0)
        
        self.style_empty_buttons()

    def build_days_frame(self):
        days = self.get_days(self.months[self.current_month_index].id)
        filler_number = 0
        for i in range(6):
            for j in range(7):
                if days :
                    day = days.pop(0)
                else:
                    day = DayDTO(id=0, number=filler_number, checked=False, month_id=0)

                self.btn_dict[(i, j)] = self.build_button(day, i, j)

        self.style_empty_buttons()
    
    # ===============================
    # TOP BAR (NAVEGAÇÃO ENTRE MESES)
    # ===============================

    def update_top_bar(self):
        current_month = self.months[self.current_month_index]

        self.month_label.configure(text=f"{current_month.year}\n{current_month.name}", text_color="white")

        update_navigation_button(self, self.prev_button, "prev", disabled=self.current_month_index == 0)

        update_navigation_button(self, self.next_button, "next", disabled=self.current_month_index >= len(self.months) - 1)

    def build_top_bar(self):
        current_month = self.months[self.current_month_index]

        self.month_label = ctk.CTkLabel(
            self.top_frame, 
            text=f"{current_month.year}\n{current_month.name}", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        self.month_label.grid(row=0, column=1, padx=5, pady=5)

        self.prev_button = build_navigation_button(self, "prev")
        self.prev_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.next_button = build_navigation_button(self, "next")
        self.next_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    # ========================
    # FRAME DE DIAS DA SEMANA
    # ========================

    def build_week_days_frame(self):
        week_days = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        for i, day in enumerate(week_days):
            label = ctk.CTkLabel(self.week_days_frame, text=day, font=ctk.CTkFont(size=15, weight="bold"), text_color="white")
            label.grid(row=0, column=i, padx=5, pady=5)

    def edit_tracker(self, name, tracker_id):
        try:
            with get_db() as db:
                tracker_repository = TrackerRepository(db)
                tracker_repository.update_tracker(tracker_id, name)
                self.build_sidebar_buttons()
                self.update_header()
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def remove_tracker(self, tracker_id):
        try:
            with get_db() as db:
                tracker_repository = TrackerRepository(db)
                tracker_repository.delete_tracker(tracker_id)
                self.build_sidebar_buttons()
        except Exception as e:
            print(f"Erro inesperado: {e}")

    # ==================
    # MÉTODOS DA SIDEBAR
    # ==================

    def open_new_tracker_popup(self, operation, tracker=None):

        if operation not in ["create", "edit"]:
            print(f"Operação inválida: {operation}")
            return
        
        window_exists = self.new_tracker_window is not None and self.new_tracker_window.winfo_exists()

        if window_exists:
            self.new_tracker_window.focus()
            return
        
        if operation == "create":
            self.new_tracker_window = AlterTrackerWindow(self, on_save=self.create_new_tracker)
        else:
            self.new_tracker_window = AlterTrackerWindow(
                self, 
                on_save=self.edit_tracker, 
                tracker_id=tracker.id, 
                tracker_name=tracker.name
            )

    def change_tracker(self, tracker_id):
        self.current_tracker_id = tracker_id
        self.months = self.get_months()
        
        self.update_top_bar()
        self.update_days_frame()
        self.update_header()

    def create_new_tracker(self, tracker_name):
        try:
            with get_db() as db:
                tracker_repository = TrackerRepository(db)
                tracker_repository.create_tracker(name=tracker_name)
                self.build_sidebar_buttons()
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.grid_forget()
        else:
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, padx=(0, 20), pady=20, sticky="nsew")
        self.sidebar_visible = not self.sidebar_visible

    # =====================
    # SIDEBAR DE MARCADORES
    # =====================

    def build_sidebar_buttons(self):
        trackers = self.get_trackers()
        self.tracker_btn = {}

        if getattr(self, "sidebar_buttons_frame", None):
            self.sidebar_buttons_frame.destroy()

        self.sidebar_buttons_frame = ctk.CTkFrame(self.sidebar_frame)
        self.sidebar_buttons_frame.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")
        

        for i, tracker in enumerate(trackers):
            self.tracker_btn[tracker.id] = build_sidebar_button(self, tracker.name, lambda t_id=tracker.id: self.change_tracker(t_id))
            self.tracker_btn[tracker.id].grid(row=i+1, column=0, padx=10, pady=10)

            edit_btn = build_sidebar_edit_button(self, lambda t=tracker: self.open_new_tracker_popup(operation="edit", tracker=t))
            edit_btn.grid(row=i+1, column=1, padx=5, pady=10)

            remove_btn = build_sidebar_remove_button(self, lambda t_id=tracker.id: self.remove_tracker(t_id))
            remove_btn.grid(row=i+1, column=2, padx=5, pady=10)

    def build_sidebar(self):
        self.sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="Marcadores", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        self.sidebar_label.grid(row=0, column=0, padx=5, pady=5)

        self.add_tracker_button = style_button(self.sidebar_frame, text="+", command=lambda: self.open_new_tracker_popup(operation="create"))
        self.add_tracker_button.grid(row=0, column=1, padx=5, pady=5)

        self.build_sidebar_buttons()
    
    # ===================
    # HEADER DA INTERFACE
    # ===================
    def update_header(self):
        tracker = self.get_tracker_by_id(self.current_tracker_id)
        self.header_label.configure(text=f"{tracker.name}", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")

    def build_header(self):
        tracker = self.get_tracker_by_id(self.current_tracker_id)
        self.header_label = ctk.CTkLabel(self.header_frame, text=f"{tracker.name}", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        self.header_label.grid(row=0, column=1, padx=5, pady=5)

        self.header_button = style_button(self.header_frame, text="≡", command=lambda: self.toggle_sidebar())
        self.header_button.grid(row=0, column=0, padx=5, pady=5, sticky = 'w')

    # =======================
    # CONSTRUÇÃO DA INTERFACE
    # =======================

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.header_frame = ctk.CTkFrame(self, corner_radius=0)
        self.header_frame.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="ew")
        self.header_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="main")
        self.header_frame.grid_rowconfigure(0 , weight=1)

        self.top_frame = ctk.CTkFrame(self, corner_radius=0)
        self.top_frame.grid(row=1, column=1, padx=20, pady=20, sticky="ew")
        self.top_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="main")
        self.top_frame.grid_rowconfigure(0 , weight=1)

        self.days_frame = ctk.CTkFrame(self, corner_radius=0)
        self.days_frame.grid(row=3, column=1, padx=20, pady=(0, 20), sticky="nsew")
        self.days_frame.grid_columnconfigure(tuple(range(7)), weight=1, uniform="days")
        self.days_frame.grid_rowconfigure(tuple(range(6)), weight=1, uniform="days")

        self.week_days_frame = ctk.CTkFrame(self, corner_radius=0)
        self.week_days_frame.grid(row=2, column=1, padx=20, pady=0, sticky="nsew")
        self.week_days_frame.grid_columnconfigure(tuple(range(7)), weight=1, uniform="week_days")
        self.week_days_frame.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, padx=(0, 20), pady=20, sticky="nsw")
        self.sidebar_frame.grid_columnconfigure(0, weight=1)

        self.build_top_bar()
        self.build_days_frame()
        self.build_week_days_frame()
        self.build_sidebar()
        self.build_header()