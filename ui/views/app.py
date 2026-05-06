import customtkinter as ctk
from controllers import CalendarController
from config import get_last_tracker_id

from ui.views.app_sidebar import SidebarView
from ui.views.app_calendar import MainCalendarView

SIDEBAR_WEIGHT = 1
MAIN_WEIGHT = 4

class CalendarApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calendário")
        self.geometry("1100x700")
        self.minsize(500, 350)

        self.controller = CalendarController()
        
        # Grid Principal do App
        self.grid_columnconfigure(0, weight=SIDEBAR_WEIGHT, uniform="window")
        self.grid_columnconfigure(1, weight=MAIN_WEIGHT, uniform="window")
        self.grid_rowconfigure(0, weight=1)

        self.build_forbidden_content()

        # Instancia a Sidebar passando os callbacks (funções que a sidebar vai "chamar" de volta)
        initial_tracker_id = get_last_tracker_id()
        self.sidebar_view = SidebarView(
            self, 
            controller=self.controller, 
            initial_tracker_id=initial_tracker_id,
            on_tracker_change=self.handle_tracker_change,
            on_toggle_visibility=self.handle_sidebar_toggle
        )
        self.sidebar_view.grid(row=0, column=0, sticky="nsew")

        # Instancia o Calendário
        self.calendar_view = MainCalendarView(
            self, 
            initial_tracker_id=initial_tracker_id,
            controller=self.controller
        )
        
        # Realiza a primeira checagem de estado para preencher os dados
        self.handle_tracker_change()

    # ==========================
    # GERENCIAMENTO DE ESTADO
    # ==========================
    def handle_sidebar_toggle(self, is_visible: bool):
        """Ajusta as colunas do app principal quando a sidebar expande/contrai"""
        if is_visible:
            self.grid_columnconfigure(0, weight=SIDEBAR_WEIGHT, uniform="window")
        else:
            self.grid_columnconfigure(0, weight=0, uniform="")

    def handle_tracker_change(self):
        """Chamado sempre que o tracker atual muda ou a lista de trackers é alterada"""
        trackers = self.controller.get_trackers()
        
        if trackers:
            self.forbidden_frame.grid_forget()
            self.calendar_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
            
        else:
            self.calendar_view.grid_forget()
            self.forbidden_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

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