import customtkinter as ctk
from ui.widgets import CustomButton, SmartScrollableFrame
from functools import partial
from constants import PRIMARY_THEME, MAIN_COLORS, TERTIARY_THEME, TEXT_COLOR, SECONDARY_THEME, LANGUAGES
from config import ThemeJSON
from dataclasses import dataclass
import i18n

DEFAULT_COLOR = 'hierophant-green'
SCROLLABLE_FRAME_SIZE = 80

class ThemeView(ctk.CTkFrame):
    def __init__(self, parent, on_color_change, on_theme_change, on_language_change):
        super().__init__(
            parent, 
            width=550, 
            height=450,
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

        self.theme_label = ctk.CTkLabel(self.current_theme_frame, font=ctk.CTkFont(size=18, weight="bold"), textvariable=self.text.LABEL)
        self.theme_label.grid(row=0, column=0, padx=(15, 5),  sticky="w")
        
        light, dark = i18n.t('theme.light'), i18n.t('theme.dark')
        self.theme_btns = ctk.CTkSegmentedButton(
            self.current_theme_frame, 
            values=[light, dark], 
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

        self.theme_btns.set(light if ThemeJSON.get_current_theme() == "light" else dark)

        for btn in self.theme_btns._buttons_dict.values():
            btn.configure(cursor="hand2")

    # def build_current_color(self):
    #     self.current_color_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=18, weight="bold"), text=self.text.CURRENT_COLOR)
    #     self.current_color_label.grid(row=2, column=0, padx=15, pady=(5, 0),  sticky="w")

    #     self.current_theme_frame = ctk.CTkFrame(self.main_frame, fg_color=TERTIARY_THEME.fg_color(), corner_radius=10)
    #     self.current_theme_frame.grid(row=3, column=0, padx=15, pady=5, sticky="ew")
    #     self.current_theme_frame.grid_columnconfigure(0, weight=1)

    #     text = PRIMARY_THEME.current_color if PRIMARY_THEME.current_color != DEFAULT_COLOR else f"{PRIMARY_THEME.current_color} {self.text.DEFAULT}"
    #     self.current_color = ctk.CTkLabel(self.current_theme_frame, font=ctk.CTkFont(size=16), text=text)
    #     self.current_color.grid(row=0, column=0, padx=10, sticky="w")

    def build_color(self):
        self.color_dict = {}

        self.color_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=18, weight="bold"), textvariable=self.text.COLORS)
        self.color_label.grid(row=4, column=0, padx=15, pady=(10, 0),  sticky="w")

        self.color_btns = SmartScrollableFrame(self.main_frame, height=SCROLLABLE_FRAME_SIZE)
        self.color_btns.grid(row=5, column=0, padx=15, pady=5, sticky="nsew")
        self.color_btns.grid_columnconfigure(0, weight=1)

        row=0
        current_col = ThemeJSON.get_current_color()
        for color in MAIN_COLORS.keys():
            text = color if color != DEFAULT_COLOR else f"{color} {self.text.DEFAULT}"
            btn = CustomButton(self.color_btns, 
                text=text, 
                command=partial(self.change_color, color), 
                main_color=color == current_col, 
                font_size=14, 
                bold=False, 
                anchor="w", 
                height=35
            )
            btn.grid(row=row, column=0, padx=(10, 0), pady=3, sticky="nswe")
            self.color_dict[color] = btn
            row+=1

            if color == DEFAULT_COLOR:
                self.default_color_btn = btn

    def build_language(self):
        self.language_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=18, weight="bold"), textvariable=self.text.LANGUAGE)
        self.language_label.grid(row=6, column=0, padx=15, pady=(10, 0),  sticky="w")

        self.language_btns = SmartScrollableFrame(self.main_frame, height=SCROLLABLE_FRAME_SIZE)
        self.language_btns.grid(row=7, column=0, padx=15, pady=5, sticky="nsew")
        self.language_btns.grid_columnconfigure(0, weight=1)

        current_lang = ThemeJSON.get_current_language()
        self.language_dict = {}

        row=0
        for short_lang, lang in LANGUAGES.items():
            btn = CustomButton(
                self.language_btns, 
                text=f'{short_lang} - {lang}', 
                command=partial(self.change_language, short_lang), 
                main_color= current_lang == short_lang, 
                font_size=14, 
                bold=False, 
                anchor="w", 
                height=35
            )
            btn.grid(row=row, column=0, padx=(10, 0), pady=3, sticky="nswe")
            self.language_dict[short_lang] = btn
            row+=1

            if current_lang == short_lang:
                self.selected_lang_btn = btn

    def build_new_year_options(self):
        self.option_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.option_frame.grid(row=8, column=0, padx=0, pady=5, sticky="nsew")
        self.option_frame.grid_columnconfigure(1, weight=1)

        self.option_label = ctk.CTkLabel(self.option_frame, font=ctk.CTkFont(size=18, weight="bold"), textvariable=self.text.OPTION_SWITCH)
        self.option_label.grid(row=0, column=0, padx=(15, 0), pady=5,  sticky="w")

        self.option_switch = ctk.CTkSwitch(self.option_frame, progress_color=PRIMARY_THEME.fg_color(), text="", command=ThemeJSON.toggle_new_year_popup_status, cursor='hand2', switch_height=25, switch_width=50)
        self.option_switch.grid(row=0, column=1, padx=20, pady=5,  sticky="w")
        
        if ThemeJSON.is_new_year_popup_hidden():
            self.option_switch.select()

    def change_color(self, color):
        ThemeJSON.save_current_color(color)
        PRIMARY_THEME.set_theme(color)
        self.back_button.reload_colors()
        self.theme_btns.configure(selected_color=PRIMARY_THEME.fg_color(), selected_hover_color=PRIMARY_THEME.hover_color())
        self.option_switch.configure(progress_color=PRIMARY_THEME.fg_color())

        # text = PRIMARY_THEME.current_color if PRIMARY_THEME.current_color != DEFAULT_COLOR else f"{PRIMARY_THEME.current_color} {self.text.DEFAULT}"
        # self.current_color.configure(text=text)

        current_col = ThemeJSON.get_current_color()
        for col, btn in self.color_dict.items():
            btn.main_color = current_col == col 
            btn.reload_colors()
        
        self.selected_lang_btn.reload_colors()
        self.on_color_change()

    def change_language(self, language):
        ThemeJSON.save_current_language(language)
        self.on_language_change()
        self.text.reload_language()
        
        light, dark = i18n.t('theme.light'), i18n.t('theme.dark')
        self.theme_btns.configure(values=[light, dark])
        self.theme_btns.set(light if ThemeJSON.get_current_theme() == "light" else dark)

        for widget in self.theme_btns.winfo_children():
            widget.configure(cursor="hand2")
        self.back_button.configure(text=i18n.t('actions.back'))

        current_lang = ThemeJSON.get_current_language()
        for lang, btn in self.language_dict.items():
            btn.main_color = current_lang == lang 
            btn.reload_colors()

            if current_lang == lang:
                self.selected_lang_btn = btn

        self.default_color_btn.configure(text=f'{DEFAULT_COLOR} {self.text.DEFAULT}')

    def change_theme(self, value):
        if value == i18n.t('theme.light'):
            ThemeJSON.save_current_theme("light")
        else:
            ThemeJSON.save_current_theme("dark")
        
        self.on_theme_change()

    def build_back_button(self):
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=9, column=0, padx=10, pady=(0, 10), sticky="nsew")
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
        # self.build_current_color()
        self.build_color()
        self.build_language()
        self.build_new_year_options()
        self.build_back_button()

    class _Theme_Texts:
        def __init__(self):
            self.LABEL = ctk.StringVar(value=i18n.t('theme.label'))
            self.CURRENT_COLOR = ctk.StringVar(value=i18n.t('theme.current_color'))
            self.COLORS = ctk.StringVar(value=i18n.t('theme.colors'))
            self.DEFAULT = i18n.t('theme.default')
            self.LANGUAGE = ctk.StringVar(value=i18n.t('theme.language'))
            self.OPTION_SWITCH = ctk.StringVar(value=i18n.t('theme.option_switch'))

        def reload_language(self):
            self.LABEL.set(i18n.t('theme.label'))
            self.CURRENT_COLOR.set(i18n.t('theme.current_color'))
            self.COLORS.set(i18n.t('theme.colors'))
            self.DEFAULT = i18n.t('theme.default')
            self.LANGUAGE.set(i18n.t('theme.language'))
            self.OPTION_SWITCH.set(i18n.t('theme.option_switch'))