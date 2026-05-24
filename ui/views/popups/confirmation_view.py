import customtkinter as ctk
from ui.widgets import CustomButton
from themes import TEXT_COLOR
import i18n

class ConfirmationView(ctk.CTkFrame):
    def __init__(self, parent, on_save, label, message):
        super().__init__(
            parent, 
            width=500, 
            height=400, 
            corner_radius=15, 
            border_width=1, 
            border_color=TEXT_COLOR
        )

        self.grid_propagate(False)

        self.parent = parent
        self.on_save = on_save
        self.label = label
        self.message = message
        self.build_ui()

    def ui(self):
        self.label_1 = ctk.CTkLabel(self, text=self.label, font=ctk.CTkFont(size=22, weight="bold"))
        self.label_1.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.label_2 = ctk.CTkLabel(self, text=self.message, font=ctk.CTkFont(size=16), text_color="grey")
        self.label_2.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent", width=500)
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid(row=98, column=1)

        self.btn_return = CustomButton(self.button_frame, text=i18n.t('actions.cancel'), font_size=15, command=self.destroy, height=35, width=250, main_color=False)
        self.btn_return.grid(row=0, column=0, padx=5, pady=10)

        self.btn_confirm = CustomButton(self.button_frame, text=i18n.t('actions.confirm'), font_size=15, command=self.save, height=35, width=250)
        self.btn_confirm.grid(row=0, column=1, padx=5, pady=10)

    def build_ui(self):
        self.grid_columnconfigure((0, 2), weight=1, uniform="main")
        self.grid_columnconfigure(1, weight=5, uniform="main")
        self.grid_rowconfigure((0, 99), weight=1, uniform="main")

        self.ui()

    def save(self):
        self.on_save()
        self.destroy()

    def _on_enter(self, event=None):
        self.save()
        
    def _on_escape(self, event=None):
        self.destroy()