import customtkinter as ctk
from ui.widgets import CustomButton
from themes import TEXT_COLOR, PRIMARY_THEME
from config import ThemeJSON
import i18n

class NewYearView(ctk.CTkFrame):
    def __init__(self, parent, on_save, year):
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
        self.year = year
        self.build_ui()

    def ui(self):
        
        self.label = ctk.CTkLabel(self, text=i18n.t('new_year.label', year=self.year), font=ctk.CTkFont(size=22, weight="bold"))
        self.label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.label = ctk.CTkLabel(self, text=i18n.t('new_year.warning'), font=ctk.CTkFont(size=16), text_color="grey")
        self.label.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent", width=500)
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid(row=4, column=1)

        self.check_hide_popup = ctk.CTkCheckBox(
            self, 
            text=f" {i18n.t('new_year.checkbox')}",
            fg_color=PRIMARY_THEME.fg_color(),
            hover_color=PRIMARY_THEME.hover_color(),
            cursor="hand2",
            font=ctk.CTkFont(size=15),
            corner_radius=5
        )
        self.check_hide_popup.grid(row=3, column=1, padx=5, pady=10)

        self.btn_return = CustomButton(self.button_frame, text=i18n.t('actions.cancel'), font_size=15, command=self.destroy, height=35, width=250, main_color=False)
        self.btn_return.grid(row=0, column=0, padx=5, pady=10)

        self.btn_confirm = CustomButton(self.button_frame, text=i18n.t('actions.confirm'), font_size=15, command=self.save, height=35, width=250)
        self.btn_confirm.grid(row=0, column=1, padx=5, pady=10)

    def build_ui(self):
        self.grid_columnconfigure((0, 2), weight=1, uniform="main")
        self.grid_columnconfigure(1, weight=3, uniform="main")
        self.grid_rowconfigure((0, 5), weight=1, uniform="main")

        self.ui()

    def save(self):
        if self.check_hide_popup.get() == 1: ThemeJSON.toggle_new_year_popup_status()
        self.on_save()
        self.destroy()