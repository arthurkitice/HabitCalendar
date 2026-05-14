import customtkinter as ctk
from config import LastTrackerJSON, CurrentThemeJSON
from services import TrackerService
from .app_sidebar import SidebarView
from .app_calendar import MainCalendarView
from functools import partial
from constants import PRIMARY_THEME

SIDEBAR_WEIGHT = 1
MAIN_WEIGHT = 4

PRIMARY_THEME.set_theme(CurrentThemeJSON.get_current_theme())

class CalendarApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calendário")
        self.geometry("1100x700")
        self.minsize(850, 450)
        
        self.tracker_service = TrackerService()

        # Grid Principal do App
        self.grid_columnconfigure(0, weight=SIDEBAR_WEIGHT, uniform="window", minsize=350)
        self.grid_columnconfigure(1, weight=MAIN_WEIGHT, uniform="window", minsize=500)
        self.grid_rowconfigure(0, weight=1, minsize=400)

        self.build_forbidden_content()

        # Instancia a Sidebar passando os callbacks (funções que a sidebar vai "chamar" de volta)
        initial_tracker_id = LastTrackerJSON.get_last_tracker_id()
        self.sidebar_view = SidebarView(
            self, 
            initial_tracker_id=initial_tracker_id,
            on_tracker_change=self.handle_tracker_change,
            on_color_change=self.handle_color_change,
            on_toggle_visibility=self.handle_sidebar_toggle
        )
        self.sidebar_view.grid(row=0, column=0, sticky="nsew")

        # Instancia o Calendário
        self.calendar_view = MainCalendarView(
            self, 
            initial_tracker_id=initial_tracker_id
        )
        
        # Realiza a primeira checagem de estado para preencher os dados
        self.handle_tracker_change()

    # ==========================
    # GERENCIAMENTO DE ESTADO
    # ==========================
    def handle_sidebar_toggle(self, is_visible: bool):
        """Ajusta as colunas do app principal quando a sidebar expande/contrai"""
        if is_visible:
            self.grid_columnconfigure(0, weight=SIDEBAR_WEIGHT, uniform="window", minsize=350)
        else:
            self.grid_columnconfigure(0, weight=0, uniform="", minsize=0)

    def handle_tracker_change(self, tracker_id=None):
        """Chamado sempre que o tracker atual muda ou a lista de trackers é alterada"""
        trackers = self.tracker_service.get_all_trackers()
        if tracker_id:
            self.calendar_view.update_tracker_data(tracker_id=tracker_id) #Averiguar a parte do diálogo entre as views
        if trackers:
            self.forbidden_frame.grid_forget()
            self.calendar_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
            
        else:
            self.calendar_view.grid_forget()
            self.forbidden_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def handle_color_change(self):
        self.sidebar_view.reload_colors()
        self.calendar_view.reload_colors()

    def build_forbidden_content(self) -> None:
        """Frame de bloqueio exibido quando não existem marcadores"""
        self.forbidden_frame = ctk.CTkFrame(self, corner_radius=0)
        self.forbidden_frame.grid_columnconfigure(0, weight=1)
        self.forbidden_frame.grid_rowconfigure(0, weight=1)

        forbidden_label = ctk.CTkLabel(
            self.forbidden_frame, 
            text="Adicione um novo marcador\nclicando no botão '+' da barra lateral\npara visualizar algum calendário",
            font=ctk.CTkFont(size=20),
            text_color="gray"
        )
        forbidden_label.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = CalendarApp()
    app.mainloop()