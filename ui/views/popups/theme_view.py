import customtkinter as ctk
from ui.widgets import CustomButton, SmartScrollableFrame
from functools import partial
from constants import PRIMARY_THEME, MAIN_COLORS
from config import CurrentThemeJSON

class ThemeView(ctk.CTkFrame):
    def __init__(self, parent, on_color_change):
        super().__init__(
            parent, 
            width=500, 
            height=400,
            corner_radius=15,
            fg_color="#242424",
            border_width=1, 
            border_color="white"
        )

        self.grid_propagate(False)

        self.parent = parent
        self.on_color_change = on_color_change
        self.build_ui()

    def build_top_bar(self):
        self.top_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=20, weight="bold"), text=f"Tema atual:")
        self.top_label.grid(row=0, column=0, padx=15, pady=(5, 0),  sticky="w")

        self.top_bar = ctk.CTkFrame(self.main_frame, fg_color="#252525", corner_radius=10)
        self.top_bar.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        self.top_bar.grid_columnconfigure(0, weight=1)

        self.current_theme_label = ctk.CTkLabel(self.top_bar, font=ctk.CTkFont(size=20), text=PRIMARY_THEME.current_color)
        self.current_theme_label.grid(row=0, column=0, padx=10, sticky="w")

    def build_themes(self):
        self.btn_dict = {}

        self.theme_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=20, weight="bold"), text="Temas:")
        self.theme_label.grid(row=2, column=0, padx=15, pady=(10, 0),  sticky="w")

        self.theme_btns = SmartScrollableFrame(self.main_frame)
        self.theme_btns.grid(row=3, column=0, padx=15, pady=5, sticky="nsew")
        self.theme_btns.grid_columnconfigure(0, weight=1)

        row=0
        for color in MAIN_COLORS.keys():
            btn = CustomButton(self.theme_btns, text=color, command=partial(self.change_color, color), main_color=False, font_size=16, bold=False, anchor="w", height=35)
            btn.grid(row=row, column=0, padx=5, pady=3, sticky="we")
            self.btn_dict[color] = btn
            row+=1

    def change_color(self, color):
        CurrentThemeJSON.save_current_theme(color)
        PRIMARY_THEME.set_theme(color)
        self.back_button.reload_colors()
        self.current_theme_label.configure(text=PRIMARY_THEME.current_color)
        self.on_color_change()

    def build_back_button(self):
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)

        self.back_button = CustomButton(self.button_frame, text="Voltar", command=self.destroy, font_size=15, height=35)
        self.back_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1, uniform="main")
        self.main_frame.grid_rowconfigure(3, weight=1)

        self.build_top_bar()
        self.build_themes()
        self.build_back_button()