import customtkinter as ctk
from config import LastTrackerJSON, ThemeJSON, TrackerDataJSON, WindowSizeJSON
from services import TrackerService
from .app_sidebar import SidebarView
from .app_calendar import MainCalendarView
from themes import PRIMARY_THEME, TEXT_COLOR
import i18n
import sys
import os
from ui.widgets import SliderButton

SIDEBAR_WEIGHT = 1
MAIN_WEIGHT = 4

class CalendarApp(ctk.CTk):
    def __init__(self, base_dir):
        super().__init__(className='HabitCalendar')

        self.base_dir = base_dir
        
        self.title("HabitCalendar")
        self._set_icon()
        self.geometry("850x500")

        if WindowSizeJSON.is_window_maximized():
            self.after(1, self._maximize)
        else:
            width, height = WindowSizeJSON.get_window_size()
            self.geometry(f"{width}x{height}")

        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.minsize(850, 500)
        self.tracker_service = TrackerService()
        self.main_container = None
        self.build_all_ui()

    def _set_icon(self):
        from PIL import Image, ImageTk
        import os

        icon_path = os.path.join(self.base_dir, 'icon.png')
        if not os.path.exists(icon_path):
            print(f"Ícone não encontrado em: {icon_path}")
            return
        
        try:
            img = Image.open(icon_path)
            self._icon = ImageTk.PhotoImage(img)
            self.wm_iconphoto(True, self._icon)

        except Exception as e:
            print(f"Erro ao setar ícone: {e}")

    def _maximize(self):
        if sys.platform.startswith('linux'):
            self._maximize_linux()
        elif sys.platform == 'win32':
            self.state('zoomed')
        elif sys.platform == 'darwin':
            self.attributes('-zoomed', True)

    def _maximize_linux(self):
        try:
            from ewmh import EWMH
            ewmh = EWMH()
            titulo = self.title().encode('utf-8')
            for w in reversed(ewmh.getClientList()):
                try:
                    if ewmh.getWmName(w) and titulo in ewmh.getWmName(w):
                        ewmh.setWmState(w, 1, '_NET_WM_STATE_MAXIMIZED_VERT', '_NET_WM_STATE_MAXIMIZED_HORZ')
                        ewmh.display.flush()
                        return
                except:
                    continue
            self.attributes('-zoomed', True)
        except:
            self.attributes('-zoomed', True)
            
    def build_all_ui(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        self.main_container.grid_columnconfigure(0, weight=SIDEBAR_WEIGHT, uniform="window", minsize=350)
        self.main_container.grid_columnconfigure(1, weight=MAIN_WEIGHT, uniform="window", minsize=500)
        self.main_container.grid_rowconfigure(0, weight=1, minsize=400)

        PRIMARY_THEME.set_theme(ThemeJSON.get_current_color())
        ctk.set_appearance_mode(ThemeJSON.get_current_theme())

        # Instancia a Sidebar dentro do MAIN_CONTAINER
        initial_tracker_id = LastTrackerJSON.get_last_tracker_id()
        self.sidebar_view = SidebarView(
            self.main_container, 
            initial_tracker_id=initial_tracker_id,
            on_tracker_change=self.handle_tracker_change,
            on_color_change=self.handle_color_change,
            on_toggle_visibility=self.handle_sidebar_toggle,
            on_year_remove=self.handle_year_remove,
            on_theme_change=self.handle_theme_change,
            on_language_change=self.handle_language_change,
            on_restore_backup=self.handle_backup_restore
        )
        self.sidebar_view.grid(row=0, column=0, sticky="nsew")

        # Instancia o Calendário dentro do MAIN_CONTAINER
        self.calendar_view = MainCalendarView(
            self.main_container, 
            initial_tracker_id=initial_tracker_id
        )

        self.build_forbidden_content()

        self.handle_tracker_change()

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
        self.forbidden_label.configure(text=i18n.t('forbidden_frame.label'))
        self.forbidden_label_info.configure(text=i18n.t('forbidden_frame.info'))

        values = self._get_forbidden_values()

        self.example_trackers.change_values(values)

    def handle_color_change(self):
        self.sidebar_view.reload_colors()
        self.calendar_view.reload_colors()
        self.example_trackers.reload_colors()

    def handle_theme_change(self):
        import tkinter as tk

        cor_fundo_atual = self._apply_appearance_mode(self.cget("fg_color"))

        cortina = tk.Frame(self, bg=cor_fundo_atual)
        cortina.place(relwidth=1.0, relheight=1.0, x=0, y=0)

        self.update() #Força o frame a aparecer na tela

        ctk.set_appearance_mode(ThemeJSON.get_current_theme())

        self.update_idletasks() #Só passa para a próxima etapa quando a fila de execução limpar
        
        # MÁGICA AQUI: Reafirma o ícone para o sistema operacional após o redesenho
        self._set_icon()

        cortina.destroy()

    def handle_year_remove(self, year: int, is_top_year: bool = True):
        if self.calendar_view.current_year != year:
            self.calendar_view.update_top_bar()
            return
   
        if is_top_year:
            month, year = 12, year-1
        else:
            month, year = 1, year+1

        TrackerDataJSON.save_current_date(self.calendar_view.current_tracker_id, month, year)
        self.calendar_view.update_tracker_data(self.calendar_view.current_tracker_id)

    def on_exit(self):
        is_maximized = False
        try:
            is_maximized = bool(self.attributes('-zoomed'))
        except:
            pass

        if is_maximized:
            WindowSizeJSON.maximize_window()
        else:
            medidas = self.geometry().split('+')[0]
            largura, altura = medidas.split('x')
            WindowSizeJSON.save_window_size(int(largura), int(altura))
            WindowSizeJSON.unmaximize_window()

        self.destroy()

    def handle_backup_restore(self):
        self.sidebar_view.build_sidebar_buttons()
        self.sidebar_view.change_to_first_tracker()
        self.calendar_view.update_calendar()
        self.handle_tracker_change()

    def build_forbidden_content(self) -> None:
        self.forbidden_frame = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.forbidden_frame.grid_columnconfigure(0, weight=1)
        self.forbidden_frame.grid_rowconfigure((0, 99), weight=1)

        self.forbidden_label = ctk.CTkLabel(
            self.forbidden_frame, 
            text=i18n.t('forbidden_frame.label'),
            font=ctk.CTkFont(size=20),
            text_color=TEXT_COLOR
        )
        self.forbidden_label.grid(row=1, column=0, pady=20, sticky="nsew")

        self.forbidden_label_info = ctk.CTkLabel(
            self.forbidden_frame, 
            text=i18n.t('forbidden_frame.info'),
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.forbidden_label_info.grid(row=2, column=0, sticky="nsew")
        
        values = self._get_forbidden_values()

        self.example_trackers = SliderButton(
            self.forbidden_frame, 
            command=self.sidebar_view.create_new_tracker,
            width=300,
            values=values, 
            font_size=15, 
            bold=False
        )
        self.example_trackers.grid(row=3, column=0, sticky='n', padx=5, pady=20)

    def _get_forbidden_values(self):
        return [
            i18n.t('forbidden_frame.example_trackers.job'), 
            i18n.t('forbidden_frame.example_trackers.college'), 
            i18n.t('forbidden_frame.example_trackers.medicine'), 
            i18n.t('forbidden_frame.example_trackers.exercises')
        ]