import customtkinter as ctk
from config import LastTrackerJSON, ThemeJSON, TrackerDataJSON
from services import TrackerService
from .app_sidebar import SidebarView
from .app_calendar import MainCalendarView
from functools import partial
from constants import PRIMARY_THEME, IconImages # <-- Importado IconImages
import os
import i18n

# 1. Caminho absoluto seguro

SIDEBAR_WEIGHT = 1
MAIN_WEIGHT = 4

class CalendarApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calendário")
        self.geometry("1100x700")
        self.minsize(850, 450)
        self.tracker_service = TrackerService()
        self.main_container = None
        self.build_all_ui()

    def build_all_ui(self, reopen_theme_popup=False):
        # Destrói o contêiner antigo, limpando a tela
        if self.main_container:
            self.main_container.destroy()

        # Cria o novo Contêiner Principal
        self.main_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        self.main_container.grid_columnconfigure(0, weight=SIDEBAR_WEIGHT, uniform="window", minsize=350)
        self.main_container.grid_columnconfigure(1, weight=MAIN_WEIGHT, uniform="window", minsize=500)
        self.main_container.grid_rowconfigure(0, weight=1, minsize=400)

        PRIMARY_THEME.set_theme(ThemeJSON.get_current_color())
        ctk.set_appearance_mode(ThemeJSON.get_current_theme())

        self.build_forbidden_content()

        # Instancia a Sidebar dentro do MAIN_CONTAINER
        initial_tracker_id = LastTrackerJSON.get_last_tracker_id()
        self.sidebar_view = SidebarView(
            self.main_container, 
            initial_tracker_id=initial_tracker_id,
            on_tracker_change=self.handle_tracker_change,
            on_color_change=self.handle_color_change,
            on_toggle_visibility=self.handle_sidebar_toggle,
            on_year_remove=self.handle_year_removal,
            on_theme_change=self.handle_theme_change,
            on_language_change=self.handle_language_change
        )
        self.sidebar_view.grid(row=0, column=0, sticky="nsew")

        # Instancia o Calendário dentro do MAIN_CONTAINER
        self.calendar_view = MainCalendarView(
            self.main_container, 
            initial_tracker_id=initial_tracker_id
        )
        
        self.handle_tracker_change()

        if reopen_theme_popup:
            self.sidebar_view.theme_popup()

    def handle_sidebar_toggle(self, is_visible: bool):
        if is_visible:
            self.main_container.grid_columnconfigure(0, weight=SIDEBAR_WEIGHT, uniform="window", minsize=350)
        else:
            self.main_container.grid_columnconfigure(0, weight=0, uniform="", minsize=0)

    def handle_tracker_change(self, tracker_id=None):
        trackers = self.tracker_service.get_all_trackers()
        if tracker_id:
            self.calendar_view.update_tracker_data(tracker_id=tracker_id) 
        if trackers:
            self.forbidden_frame.grid_forget()
            self.calendar_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        else:
            self.calendar_view.grid_forget()
            self.forbidden_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def handle_language_change(self):
        i18n.set('locale', ThemeJSON.get_current_language())
        self.calendar_view.reload_language()
        self.sidebar_view.reload_language()

    def handle_color_change(self):
        self.sidebar_view.reload_colors()
        self.calendar_view.reload_colors()

    def handle_theme_change(self):
        # 1. PEGA A COR ATUAL DO FUNDO DO APP
        cor_fundo_atual = self._apply_appearance_mode(self.cget("fg_color"))
        
        # 2. DESCE A CORTINA (Um frame liso cobrindo 100% da tela)
        cortina = ctk.CTkFrame(self, fg_color=cor_fundo_atual, corner_radius=0)
        cortina.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        
        # Força o sistema operacional a desenhar a cortina AGORA, antes de travar
        self.update() 

        # 3. TROCA O CENÁRIO POR TRÁS DA CORTINA (Recria a UI)
        self.build_all_ui(reopen_theme_popup=True)

        # 4. GARANTE QUE A CORTINA CONTINUE NA FRENTE APÓS RECONSTRUIR A UI
        cortina.lift()
        self.update() # Força as novas cores a renderizarem quietinhas lá atrás

        # 5. SOBE A CORTINA (Destrói o frame)
        cortina.destroy()

    def handle_year_removal(self, year: int, is_top_year: bool = True):
        if self.calendar_view.current_year != year:
            return
   
        if is_top_year:
            month, year = 12, year-1
        else:
            month, year = 1, year+1

        TrackerDataJSON.save_current_date(self.calendar_view.current_tracker_id, month, year)
        self.calendar_view.update_tracker_data(self.calendar_view.current_tracker_id)

    def build_forbidden_content(self) -> None:
        self.forbidden_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.forbidden_frame.grid_columnconfigure(0, weight=1)
        self.forbidden_frame.grid_rowconfigure(0, weight=1)

        forbidden_label = ctk.CTkLabel(
            self.forbidden_frame, 
            text="Adicione um novo marcador\nclicando no botão '+' da barra lateral\npara visualizar algum calendário",
            font=ctk.CTkFont(size=20),
            text_color="gray"
        )
        forbidden_label.grid(row=0, column=0, sticky="nsew")