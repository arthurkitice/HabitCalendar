import customtkinter as ctk
from ui.widgets import CustomButton, SmartScrollableFrame
from functools import partial
from constants import PRIMARY_THEME, MAIN_COLORS, TERTIARY_THEME, TEXT_COLOR, SECONDARY_THEME, LANGUAGES
from config import ThemeJSON
from dataclasses import dataclass
import i18n

DEFAULT_THEME = 'hierophant-green'

class ThemeView(ctk.CTkFrame):
    def __init__(self, parent, on_color_change, on_theme_change, on_language_change):
        super().__init__(
            parent, 
            width=600, 
            height=500,
            corner_radius=15,
            border_width=1, 
            border_color=TEXT_COLOR
        )

        self.grid_propagate(False)

        self.parent = parent
        self.on_color_change = on_color_change
        self.on_theme_change = on_theme_change
        self.on_language_change = on_language_change

        self.text = self._Theme_Texts()

        self.build_ui()

    def build_themes(self):
        self.current_theme_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="transparent")
        self.current_theme_frame.grid(row=1, column=0, padx=0, pady=10, sticky="ew")
        self.current_theme_frame.grid_columnconfigure(1, weight=1)

        self.theme_label = ctk.CTkLabel(self.current_theme_frame, font=ctk.CTkFont(size=18, weight="bold"), text=self.text.LABEL)
        self.theme_label.grid(row=0, column=0, padx=(15, 5),  sticky="w")

        self.theme_btns = ctk.CTkSegmentedButton(
            self.current_theme_frame, 
            values=[self.text.LIGHT_LABEL, self.text.DARK_LABEL], 
            command=self.change_theme, 
            text_color=TEXT_COLOR,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=SECONDARY_THEME.fg_color(),
            unselected_color=TERTIARY_THEME.fg_color(),
            unselected_hover_color=TERTIARY_THEME.hover_color(),
            selected_color=PRIMARY_THEME.fg_color(),
            selected_hover_color=PRIMARY_THEME.hover_color(),
        )
        self.theme_btns.grid(row=0, column=1, padx=(5, 15), sticky="nsew")

        self.theme_btns.set(self.text.LIGHT_LABEL if ThemeJSON.get_current_theme() == "light" else self.text.DARK_LABEL)

        for btn in self.theme_btns._buttons_dict.values():
            btn.configure(cursor="hand2")

    def build_current_color(self):
        self.current_color_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=18, weight="bold"), text=self.text.CURRENT_COLOR)
        self.current_color_label.grid(row=2, column=0, padx=15, pady=(5, 0),  sticky="w")

        self.current_theme_frame = ctk.CTkFrame(self.main_frame, fg_color=TERTIARY_THEME.fg_color(), corner_radius=10)
        self.current_theme_frame.grid(row=3, column=0, padx=15, pady=5, sticky="ew")
        self.current_theme_frame.grid_columnconfigure(0, weight=1)

        text = PRIMARY_THEME.current_color if PRIMARY_THEME.current_color != DEFAULT_THEME else f"{PRIMARY_THEME.current_color} {self.text.DEFAULT}"
        self.current_color = ctk.CTkLabel(self.current_theme_frame, font=ctk.CTkFont(size=16), text=text)
        self.current_color.grid(row=0, column=0, padx=10, sticky="w")

    def build_color(self):
        self.btn_dict = {}

        self.color_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=18, weight="bold"), text=self.text.COLORS)
        self.color_label.grid(row=4, column=0, padx=15, pady=(10, 0),  sticky="w")

        self.color_btns = SmartScrollableFrame(self.main_frame, height=75)
        self.color_btns.grid(row=5, column=0, padx=15, pady=5, sticky="nsew")
        self.color_btns.grid_columnconfigure(0, weight=1)

        row=0
        for color in MAIN_COLORS.keys():
            text = color if color != DEFAULT_THEME else f"{color} {self.text.DEFAULT}"
            btn = CustomButton(self.color_btns, text=text, command=partial(self.change_color, color), main_color=False, font_size=14, bold=False, anchor="w", height=35)
            btn.grid(row=row, column=0, padx=(10, 0), pady=3, sticky="nswe")
            self.btn_dict[color] = btn
            row+=1

    def build_language(self):
        self.language_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=18, weight="bold"), text=self.text.LANGUAGE)
        self.language_label.grid(row=6, column=0, padx=15, pady=(10, 0),  sticky="w")

        self.language_btns = SmartScrollableFrame(self.main_frame, height=75)
        self.language_btns.grid(row=7, column=0, padx=15, pady=5, sticky="nsew")
        self.language_btns.grid_columnconfigure(0, weight=1)

        current_lang = ThemeJSON.get_current_language()
        self.language_dict = {}

        row=0
        for sigil, lang in LANGUAGES.items():
            btn = CustomButton(
                self.language_btns, 
                text=f'{sigil} - {lang}', 
                command=partial(self.change_language, sigil), 
                main_color= current_lang == sigil, 
                font_size=14, 
                bold=False, 
                anchor="w", 
                height=35
            )
            btn.grid(row=row, column=0, padx=(10, 0), pady=3, sticky="nswe")
            self.language_dict[sigil] = btn
            row+=1

    def change_color(self, color):
        ThemeJSON.save_current_color(color)
        PRIMARY_THEME.set_theme(color)
        self.back_button.reload_colors()
        self.current_color_label.configure(text=PRIMARY_THEME.current_color if color != DEFAULT_THEME else f"{color} {self.text.DEFAULT}")
        self.theme_btns.configure(selected_color=PRIMARY_THEME.fg_color(), selected_hover_color=PRIMARY_THEME.hover_color())
        current_lang = ThemeJSON.get_current_language()
        for key, btn in self.language_dict.items():
            if current_lang == key:
                btn.main_color = True
                btn.reload_colors()
                break
        self.on_color_change()

    def change_language(self, language):
        ThemeJSON.save_current_language(language)
        self.on_language_change()
        self.destroy()

    def change_theme(self, value):
        if value == self.text.LIGHT_LABEL:
            ThemeJSON.save_current_theme("light")
        else:
            ThemeJSON.save_current_theme("dark")
        self.on_theme_change()

    def build_back_button(self):
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=8, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)

        self.back_button = CustomButton(self.button_frame, text=i18n.t('actions.back'), command=self.destroy, font_size=15, height=35)
        self.back_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.build_themes()
        self.build_current_color()
        self.build_color()
        self.build_language()
        self.build_back_button()

    class _Theme_Texts:
        def __init__(self):
            self.LABEL = i18n.t('theme.label')
            self.LIGHT_LABEL = i18n.t('theme.light')
            self.DARK_LABEL = i18n.t('theme.dark')
            self.CURRENT_COLOR = i18n.t('theme.current_color')
            self.COLORS = i18n.t('theme.colors')
            self.DEFAULT = i18n.t('theme.default')
            self.LANGUAGE = i18n.t('theme.language')
            self.CURRENT_LANGUAGE = i18n.t('theme.current_language')