import customtkinter as ctk
from functools import partial
from config import LastTrackerJSON, TrackerDataJSON, CurrentThemeJSON
from ui.widgets import SidebarButton, CustomButton, SmartScrollableFrame, IconButton
from constants import IconType, MAIN_COLORS
from dtos import TrackerDTO
from services import TrackerService
from ..popups import PopupHandler

class SidebarView(ctk.CTkFrame):
    def __init__(self, parent, initial_tracker_id, on_tracker_change, on_color_change, on_toggle_visibility, on_year_remove):
        super().__init__(parent, fg_color="transparent")
        
        self.tracker_service = TrackerService()

        self.current_tracker_id = initial_tracker_id
        
        # Callbacks para avisar o App.py do que aconteceu aqui dentro
        self.on_tracker_change = on_tracker_change
        self.on_color_change = on_color_change
        self.on_toggle_visibility = on_toggle_visibility 
        self.on_year_remove = on_year_remove
        
        self.sidebar_visible = True
        self.tracker_btn = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.build_ui()
        self.update_sidebar()

    # ==================
    # MÉTODOS DA SIDEBAR
    # ==================
    def edit_tracker(self, name: str, tracker_id: int) -> None:
        self.tracker_service.update_tracker(tracker_id, name)
        tracker = self.tracker_service.get_tracker_by_id(tracker_id)
        self.on_color_change()
        for frame in self.btn_list:
            if frame.tracker.id == tracker_id:
                frame.tracker = tracker
                frame.tracker_btn.configure(text=tracker.name)
        self.update_sidebar()

    def remove_tracker(self, tracker_id: int) -> None:
        self.tracker_service.delete_tracker(tracker_id)
        trackers = self.tracker_service.get_all_trackers()
        last_tracker_id = trackers[-1].id if trackers else 0

        removed = False
        for i, frame in enumerate(self.btn_list):
            if removed:
                frame.grid(row=i-1, column=0, sticky="nsew")
            elif frame.tracker.id == tracker_id:
                frame.destroy()
                removed_index = i
                removed = True

        if removed_index: self.btn_list.pop(removed_index)
        
        TrackerDataJSON.remove_tracker_data(tracker_id)

        if last_tracker_id == 0 or tracker_id == self.current_tracker_id:
            self.change_tracker(last_tracker_id)

    def open_new_tracker_popup(self, tracker: TrackerDTO | None = None) -> None:
        if tracker:
            PopupHandler.alter_tracker_popup(self, tracker_name=tracker.name, tracker_id=tracker.id, on_save=self.edit_tracker)
        else:
            PopupHandler.alter_tracker_popup(self, on_save=self.create_new_tracker)

    def open_tracker_view_popup(self, tracker: TrackerDTO | None = None) -> None:
        PopupHandler.tracker_popup(self, tracker.name, tracker.id, self.on_year_remove)

    def theme_popup(self):
        PopupHandler.theme_popup(self, self.on_color_change)

    def open_delete_tracker_popup(self, tracker: TrackerDTO | None = None) -> None:
        PopupHandler.delete_tracker_popup(self, on_save=partial(self.remove_tracker, tracker.id), tracker_name=tracker.name)

    def change_tracker(self, tracker_id: int) -> None:
        self.current_tracker_id = tracker_id
        LastTrackerJSON.save_current_tracker_id(self.current_tracker_id)
        self.reload_colors()
        self.update_sidebar()
        self.on_tracker_change(tracker_id)

    def create_new_tracker(self, tracker_name: str) -> None:
        new_tracker = self.tracker_service.create_tracker(tracker_name)
        TrackerDataJSON.save_current_date(new_tracker.id)
        self.build_button_row(new_tracker, len(self.btn_list))

        if self.current_tracker_id == 0:
            trackers = self.tracker_service.get_all_trackers()
            self.current_tracker_id = trackers[0].id if trackers else 0
            self.change_tracker(self.current_tracker_id)

    def toggle_sidebar(self) -> None:
        if self.sidebar_visible:
            self.sidebar_frame.grid_forget()
            self.reduced_sidebar_frame.grid(row=0, column=0, sticky="nsew")
        else:
            self.reduced_sidebar_frame.grid_forget()
            self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
            
        self.sidebar_visible = not self.sidebar_visible
        # Avisa o app.py para mudar os pesos (uniform="") da coluna principal
        self.on_toggle_visibility(self.sidebar_visible)

    # =====================
    # CONSTRUÇÃO DOS FRAMES
    # =====================
    def build_sidebar_buttons(self) -> None:
        trackers = self.tracker_service.get_all_trackers()

        if getattr(self, "sidebar_buttons_frame", None):
            self.sidebar_buttons_frame.destroy()

        self.sidebar_buttons_frame = SmartScrollableFrame(self.sidebar_frame, corner_radius=0)
        self.sidebar_buttons_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.sidebar_buttons_frame.grid_columnconfigure(0, weight=1)

        if not trackers: return

        self.btn_list: list[ctk.CTkFrame] = []

        for i, tracker in enumerate(trackers):
            self.build_button_row(tracker, i)

        self.reload_colors()

    def build_button_row(self, tracker, i):
        btn_frame = ctk.CTkFrame(self.sidebar_buttons_frame, fg_color="transparent")
        btn_frame.grid(row=i, column=0, sticky="nsew")
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.tracker = tracker

        btn_frame.selected_line = ctk.CTkFrame(btn_frame, height=40, width=15, fg_color="transparent", corner_radius=0)
        btn_frame.selected_line.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        btn_frame.tracker_btn = SidebarButton(btn_frame, tracker=tracker.name, command=lambda f=btn_frame: self.change_tracker(f.tracker.id))
        btn_frame.tracker_btn.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="we")

        btn_frame.edit_btn = SidebarButton(btn_frame, command=lambda f=btn_frame: self.open_new_tracker_popup(f.tracker), icon_type=IconType.EDIT)
        btn_frame.edit_btn.grid(row=0, column=2, padx=5, pady=10, sticky="we")

        btn_frame.remove_btn = SidebarButton(btn_frame, command=lambda f=btn_frame: self.open_delete_tracker_popup(f.tracker), icon_type=IconType.REMOVE)
        btn_frame.remove_btn.grid(row=0, column=3, padx=5, pady=10, sticky="we")

        btn_frame.config_btn = SidebarButton(btn_frame, command=lambda f=btn_frame: self.open_tracker_view_popup(f.tracker), icon_type=IconType.CONFIG)
        btn_frame.config_btn.grid(row=0, column=4, padx=(5, 20), pady=10, sticky="we")

        self.btn_list.append(btn_frame)

    def update_sidebar(self) -> None:
        tracker = self.tracker_service.get_tracker_by_id(tracker_id=self.current_tracker_id)
        tracker_text = tracker.name if tracker is not None else "Nenhum"
        self.tracker_label.configure(text=f"Marcador atual:\n{tracker_text if len(tracker_text) < 50 else tracker_text[:47] + '...'}")

    def build_full_sidebar(self) -> None:
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        self.sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="Marcadores", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        self.sidebar_label.grid(row=0, column=0, padx=(25, 10), pady=5, sticky= "nsew")

        self.spacer_button = IconButton(self.sidebar_frame, command=self.theme_popup, icon_type=IconType.PALLETE, height=30, width=44)
        self.spacer_button.grid(row=0, column=2, padx=5, pady=5)

        self.add_tracker_button = CustomButton(self.sidebar_frame, text="+", command=self.open_new_tracker_popup, height=30, width=44)
        self.add_tracker_button.grid(row=0, column=1, padx=5, pady=5)

        self.hide_sidebar_button = CustomButton(self.sidebar_frame, text="<", command=self.toggle_sidebar, width=44, height=30, main_color=False)
        self.hide_sidebar_button.grid(row=0, column=3, padx=(5, 25), pady=5, sticky = "w")

        #fg_color transparente pois evita "flashes" ao abrir e fechar a barra. Posteriormente alterada com o reload_colors()
        self.background_tracker_frame = ctk.CTkFrame(self.sidebar_frame, corner_radius=0, fg_color="transparent")
        self.background_tracker_frame.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.background_tracker_frame.grid_columnconfigure(0, weight=1)

        self.tracker_frame = ctk.CTkFrame(self.background_tracker_frame, corner_radius=0)
        self.tracker_frame.grid(row=2, column=0, columnspan=4, padx=0, pady=3, sticky="nsew")
        self.tracker_frame.grid_columnconfigure(0, weight=1)

        self.tracker_label = ctk.CTkLabel(self.tracker_frame, text="", font=ctk.CTkFont(size=20, weight="bold"), text_color="white", wraplength=325)
        self.tracker_label.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")

        self.build_sidebar_buttons()

    def build_reduced_sidebar(self) -> None:
        self.reduced_sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.reduced_sidebar_frame.grid_columnconfigure(0, weight=1)
        
        self.toggle_button = CustomButton(
            self.reduced_sidebar_frame, 
            text=">", 
            command=self.toggle_sidebar, 
            width=40,
            fg_color="transparent",
            main_color=False
        )
        self.toggle_button.grid(row=0, column=0, padx=0, pady=5, sticky="w")

    def build_ui(self) -> None:
        self.build_reduced_sidebar()
        self.build_full_sidebar()

    def reload_colors(self):
        self.add_tracker_button.reload_colors()
        color = MAIN_COLORS[CurrentThemeJSON.get_current_theme()]["fg"]
        for frame in self.btn_list:
            frame.selected_line.configure(fg_color=color if frame.tracker.id == self.current_tracker_id else "transparent")
        self.background_tracker_frame.configure(fg_color=color)