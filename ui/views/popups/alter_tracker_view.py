import customtkinter as ctk
from ui.widgets import CustomButton
from services import TrackerService
from config import TrackerDataJSON
from constants import TEXT_COLOR
import i18n

class AlterTrackerFrame(ctk.CTkFrame):
    def __init__(self, parent, on_save, tracker_name=None, tracker_id=None):
        super().__init__(parent, width=500, height=400, corner_radius=15, border_width=1, border_color=TEXT_COLOR)

        self.grid_propagate(False)

        self.parent = parent
        self.on_save = on_save
        self.tracker_id = tracker_id
        self.tracker_name = tracker_name

        self.current_color = None
        self._yml_path = 'alter_tracker'

        self.build_ui()

    def ui_new_tracker(self):
        text = i18n.t(f'{self._yml_path}.new_tracker')
        self.label = ctk.CTkLabel(self.main_frame, text=text, font=ctk.CTkFont(size=22, weight="bold"))
        self.label.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        text = i18n.t(f'{self._yml_path}.new_tracker_placeholder')
        self.entry = ctk.CTkEntry(self.main_frame, placeholder_text=text, height=35)
        self.entry.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    def ui_edit_tracker(self, tracker_name):
        tracker = tracker_name if len(tracker_name) < 15 else f"{tracker_name[:15]}..."

        text = i18n.t(f'{self._yml_path}.edit_tracker', tracker=tracker)
        self.label = ctk.CTkLabel(self.main_frame, text=text, font=ctk.CTkFont(size=22, weight="bold"))
        self.label.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        text = i18n.t(f'{self._yml_path}.name')
        self.name_label = ctk.CTkLabel(self.main_frame, text=text, font=ctk.CTkFont(size=16, weight="bold"))
        self.name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        text = i18n.t(f'{self._yml_path}.edit_tracker_placeholder')
        self.entry = ctk.CTkEntry(self.main_frame, placeholder_text=text, height=35)
        self.entry.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        self.build_color_buttons()

        self.entry.insert(0, tracker_name)

        self.main_frame.update_idletasks()

    def build_color_buttons(self):
        from constants import TRACKER_COLORS
        from functools import partial

        text = i18n.t(f'{self._yml_path}.color')
        self.color_label = ctk.CTkLabel(self.main_frame, text=text, font=ctk.CTkFont(size=16, weight="bold"))
        self.color_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        MAX_COLUMNS = 4
        self.color_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.color_frame.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="nsew")
        self.color_frame.grid_columnconfigure(tuple(range(MAX_COLUMNS)), weight=1)

        self.btn_list: list[ctk.CTkButton] = []

        for i, color in enumerate(TRACKER_COLORS.keys()):
            btn = ctk.CTkButton(
                self.color_frame,
                text="", 
                corner_radius=100, 
                command=partial(self.set_color, color), 
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

        self.set_color(TrackerDataJSON.get_color(self.tracker_id))
    
    def set_color(self, color):
        self.current_color = color
        for btn in self.btn_list:
            btn.configure(border_width=3 if btn.color == color else 0)

    def build_ui(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=1, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure((0, 2), weight=1, uniform="main")
        self.grid_columnconfigure(1, weight=3, uniform="main")
        self.grid_rowconfigure((0, 5), weight=1, uniform="main")

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent", width=500)
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid(row=2, column=1)

        self.btn_return = CustomButton(self.button_frame, text=i18n.t('actions.cancel'), font_size=15, command=self.destroy, height=35, width=250, main_color=False)
        self.btn_return.grid(row=0, column=0, padx=5, pady=10)

        self.btn_confirm = CustomButton(self.button_frame, text=i18n.t('actions.save'), font_size=15, command=self.save, height=35, width=250)
        self.btn_confirm.grid(row=0, column=1, padx=5, pady=10)

        self.error_msg = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=12), text_color="grey")
        
        if self.tracker_name:
            self.ui_edit_tracker(self.tracker_name)
        else:
            self.ui_new_tracker()

    def save(self):
        text = self.entry.get().split()

        if not text:
            self.error_msg.grid(row=3, column=0, padx=5, pady=0, sticky="w")
            self.error_msg.configure(text=i18n.t(f'{self._yml_path}.warning1'))
            return
        
        text = ' '.join(text)

        if self.tracker_name != text and TrackerService().get_tracker_by_name(text):
            self.error_msg.grid(row=3, column=0, padx=5, pady=0, sticky="w")
            self.error_msg.configure(text=i18n.t(f'{self._yml_path}.warning2'))
            return

        if self.tracker_id is not None:
            TrackerDataJSON.save_color(self.tracker_id, self.current_color)
            self.on_save(text, self.tracker_id)
        else:
            self.on_save(text)
        self.destroy()