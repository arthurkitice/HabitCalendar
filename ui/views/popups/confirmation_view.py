import customtkinter as ctk
from ui.widgets import PopupFrame

class ConfirmationView(PopupFrame):
    def __init__(self, parent, on_save, label, message):
        super().__init__(parent, on_confirm=on_save, main_col=1)

        self.parent = parent
        self.on_save = on_save
        self.label = label
        self.message = message
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(100, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(100, weight=1)
        self.main_frame.configure(fg_color="transparent")
        self.build_ui()

    def build_labels(self):
        self.label_1 = ctk.CTkLabel(self.main_frame, text=self.label, font=ctk.CTkFont(size=22, weight="bold"))
        self.label_1.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.label_2 = ctk.CTkLabel(self.main_frame, text=self.message, font=ctk.CTkFont(size=16), text_color="grey")
        self.label_2.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

    def build_ui(self):
        self.build_labels()
        self.build_back_confirm_buttons()
