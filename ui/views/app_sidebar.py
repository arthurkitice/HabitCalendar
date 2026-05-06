import customtkinter as ctk
from functools import partial
from ui.views.new_tracker_view import AlterTrackerFrame
from config import save_current_tracker_id
from ui.widgets import SidebarButton, style_button
from constants import Operation, IconType
from controllers import CalendarController
from dtos import TrackerDTO

class SidebarView(ctk.CTkFrame):
    def __init__(self, parent, controller: CalendarController, initial_tracker_id, on_tracker_change, on_toggle_visibility):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.current_tracker_id = initial_tracker_id
        
        # Callbacks para avisar o App.py do que aconteceu aqui dentro
        self.on_tracker_change = on_tracker_change
        self.on_toggle_visibility = on_toggle_visibility 
        
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
        self.controller.edit_tracker(tracker_id, name)
        self.build_sidebar_buttons()
        self.update_sidebar()
        self.on_tracker_change() # Avisa o app.py

    def remove_tracker(self, tracker_id: int) -> None:
        self.controller.remove_tracker(tracker_id)
        trackers = self.controller.get_trackers()
        last_tracker_id = trackers[-1].id if trackers else 0

        if last_tracker_id == 0 or tracker_id == self.current_tracker_id:
            self.change_tracker(last_tracker_id)
        
        self.build_sidebar_buttons()
        self.on_tracker_change()

    def open_new_tracker_popup(self, operation: Operation, tracker: TrackerDTO | None = None) -> None:
        if getattr(self, "popup_frame", None) and self.popup_frame.winfo_exists():
            self.popup_frame.destroy()
        
        if operation == Operation.CREATE:
            self.popup_frame = AlterTrackerFrame(self, on_save=self.create_new_tracker)
        else:
            self.popup_frame = AlterTrackerFrame(
                self, on_save=self.edit_tracker, tracker_id=tracker.id, tracker_name=tracker.name
            )
        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.popup_frame.wait_visibility()
        self.popup_frame.grab_set()

    def change_tracker(self, tracker_id: int) -> None:
        self.current_tracker_id = tracker_id
        save_current_tracker_id(self.current_tracker_id)
        self.update_sidebar()
        self.on_tracker_change()

    def create_new_tracker(self, tracker_name: str) -> None:
        self.controller.create_tracker(tracker_name)
        self.build_sidebar_buttons()

        if self.current_tracker_id == 0:
            trackers = self.controller.get_trackers()
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
        trackers = self.controller.get_trackers()
        if getattr(self, "sidebar_buttons_frame", None):
            self.sidebar_buttons_frame.destroy()

        self.sidebar_buttons_frame = ctk.CTkFrame(self.sidebar_frame, corner_radius=0)
        self.sidebar_buttons_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.sidebar_buttons_frame.grid_columnconfigure(0, weight=1)

        if not trackers: return

        for i, tracker in enumerate(trackers):
            self.tracker_btn[tracker.id] = SidebarButton(self.sidebar_buttons_frame, tracker=tracker.name, command=partial(self.change_tracker, tracker.id))
            self.tracker_btn[tracker.id].grid(row=i+1, column=0, padx=10, pady=10, sticky="we")

            edit_btn = SidebarButton(self.sidebar_buttons_frame, command=partial(self.open_new_tracker_popup, Operation.EDIT, tracker), icon_type=IconType.EDIT)
            edit_btn.grid(row=i+1, column=1, padx=5, pady=10, sticky="we")

            remove_btn = SidebarButton(self.sidebar_buttons_frame, command=partial(self.remove_tracker, tracker.id), icon_type=IconType.REMOVE)
            remove_btn.grid(row=i+1, column=2, padx=5, pady=10, sticky="we")

    def update_sidebar(self) -> None:
        tracker = self.controller.get_tracker_by_id(tracker_id=self.current_tracker_id)
        tracker_text = tracker.name if tracker is not None else "Nenhum"
        self.tracker_label.configure(text=f"Marcador atual:\n{tracker_text}")

    def build_full_sidebar(self) -> None:
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        self.sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="Marcadores", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        self.sidebar_label.grid(row=0, column=0, padx=5, pady=5)

        self.add_tracker_button = style_button(
            self.sidebar_frame, 
            text="+", 
            command=partial(self.open_new_tracker_popup, Operation.CREATE), 
            width=50,
            font=ctk.CTkFont(size=20, weight="bold"), 
            fg_color="transparent"
        )
        self.add_tracker_button.grid(row=0, column=1, padx=5, pady=5)

        self.hide_sidebar_button = style_button(
            self.sidebar_frame, 
            text="<", 
            command=self.toggle_sidebar, 
            width=50,
            font=ctk.CTkFont(size=20, weight="bold"), 
            fg_color="transparent"
        )
        self.hide_sidebar_button.grid(row=0, column=2, padx=5, pady=5, sticky = "w")

        self.tracker_frame = ctk.CTkFrame(self.sidebar_frame, corner_radius=0)
        self.tracker_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.tracker_frame.grid_columnconfigure(0, weight=1)

        self.tracker_label = ctk.CTkLabel(self.tracker_frame, text="", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        self.tracker_label.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")

        self.build_sidebar_buttons()

    def build_reduced_sidebar(self) -> None:
        self.reduced_sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.reduced_sidebar_frame.grid_columnconfigure(0, weight=1)
        
        self.toggle_button = style_button(
            self.reduced_sidebar_frame, 
            text=">", 
            command=self.toggle_sidebar, 
            width=40, 
            font=ctk.CTkFont(size=20, weight="bold"), 
            fg_color="transparent"
        )
        self.toggle_button.grid(row=0, column=0, padx=0, pady=5, sticky="w")

    def build_ui(self) -> None:
        self.build_reduced_sidebar()
        self.build_full_sidebar()