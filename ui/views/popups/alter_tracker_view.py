import customtkinter as ctk
from services import TrackerService
from config import TrackerDataJSON
from themes import TRACKER_COLORS
from functools import partial
from .base_popup import PopupFrame
import i18n

class AlterTrackerFrame(PopupFrame):
    def __init__(self, parent, on_save, tracker_name=None, tracker_id=None):
        super().__init__(parent, main_col=1)

        self.parent = parent
        self.on_save = on_save
        self.tracker_id = tracker_id
        self.tracker_name = tracker_name

        self.current_color = None
        self._translation_path = 'alter_tracker'

        self.main_frame.configure(fg_color = "transparent")

        self.build_ui()

    # --- Métodos de construção ---

    def ui_new_tracker(self):
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(100, weight=1)

        text = i18n.t(f'{self._translation_path}.new_tracker')
        self.label = ctk.CTkLabel(self.main_frame, text=text, font=ctk.CTkFont(size=22, weight="bold"))
        self.label.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

        text = i18n.t(f'{self._translation_path}.new_tracker_placeholder')
        self.entry = ctk.CTkEntry(self.main_frame, placeholder_text=text, height=35)
        self.entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

    def ui_edit_tracker(self, tracker_name):
        tracker = tracker_name if len(tracker_name) < 15 else f"{tracker_name[:15]}..."

        text = i18n.t(f'{self._translation_path}.edit_tracker', tracker=tracker)
        self.label = ctk.CTkLabel(self.main_frame, text=text, font=ctk.CTkFont(size=22, weight="bold"))
        self.label.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        text = i18n.t(f'{self._translation_path}.name')
        self.name_label = ctk.CTkLabel(self.main_frame, text=text, font=ctk.CTkFont(size=16, weight="bold"))
        self.name_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        text = i18n.t(f'{self._translation_path}.edit_tracker_placeholder')
        self.entry = ctk.CTkEntry(self.main_frame, placeholder_text=text, height=35)
        self.entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.build_color_buttons()

        self.entry.insert(0, tracker_name)

        self.main_frame.update_idletasks()

    def build_color_buttons(self):
        text = i18n.t(f'{self._translation_path}.color')
        self.color_label = ctk.CTkLabel(self.main_frame, text=text, font=ctk.CTkFont(size=16, weight="bold"))
        self.color_label.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        MAX_COLUMNS = 4
        self.color_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.color_frame.grid(row=5, column=1, padx=5, pady=(0, 10), sticky="nsew")
        self.color_frame.grid_columnconfigure(tuple(range(MAX_COLUMNS)), weight=1)

        self.btn_list: list[ctk.CTkButton] = []

        for i, color in enumerate(TRACKER_COLORS.keys()):
            btn = ctk.CTkButton(
                self.color_frame,
                text="", 
                corner_radius=100, 
                command=partial(self._set_color, color), 
                fg_color=TRACKER_COLORS[color]["fg"],
                hover_color=TRACKER_COLORS[color]["hover"],
                cursor="hand2",
                border_color='white',
                width=40,
                height=40
            )
            btn.grid(row=i//MAX_COLUMNS, column = i%MAX_COLUMNS, padx=10, pady=5)
            btn.color = color

            self.btn_list.append(btn)

        self._set_color(TrackerDataJSON.get_color(self.tracker_id))

    def build_ui(self):
        self.main_frame.grid_columnconfigure((0, 2), weight=1)

        self.build_back_confirm_buttons(back_button_text=i18n.t('actions.cancel'), confirm_button_text=i18n.t('actions.save'))
        self.button_frame.grid(row=99, column=1, padx=0, pady=(10, 0), sticky='nwse')

        self.error_msg = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=12), text_color="grey")
        
        if self.tracker_name:
            self.ui_edit_tracker(self.tracker_name)
        else:
            self.ui_new_tracker()

    # --- Utilitários ---

    def save(self):
        text = self.entry.get().split()

        if not text:
            self._show_error(i18n.t(f'{self._translation_path}.warning1'))
            return
        
        text = ' '.join(text)

        if self.tracker_name != text and TrackerService().get_tracker_by_name(text):
            self._show_error(i18n.t(f'{self._translation_path}.warning2'))
            return

        if self.tracker_id is not None:
            TrackerDataJSON.save_color(self.tracker_id, self.current_color)
            self.on_save(text, self.tracker_id)
        else:
            self.on_save(text)
            
        self.destroy()

    def _show_error(self, msg):
        self.error_msg.grid(row=3, column=1, padx=5, pady=0, sticky="w")
        self.error_msg.configure(text=msg)

    def _set_color(self, color):
        self.current_color = color
        for btn in self.btn_list:
            btn.configure(border_width=3 if btn.color == color else 0)