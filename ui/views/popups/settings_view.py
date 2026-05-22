import customtkinter as ctk
from ui.widgets import CustomButton, SmartScrollableFrame, IconButton
from functools import partial
from icons import IconType
from themes import PRIMARY_THEME, MAIN_COLORS, TERTIARY_THEME, TEXT_COLOR, SECONDARY_THEME
from constants import LANGUAGES
from config import ThemeJSON
from dataclasses import dataclass
import i18n

DEFAULT_COLOR = 'pink-man'
SCROLLABLE_FRAME_SIZE = 85

class SettingsView(ctk.CTkFrame):
    def __init__(self, parent, on_color_change, on_theme_change, on_language_change):
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
        self.on_color_change = on_color_change
        self.on_theme_change = on_theme_change
        self.on_language_change = on_language_change
        self.popup_frame = None

        self.text = self._Theme_Texts()

        self.build_ui()

    def build_buttons(self):
        self.settings_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=18, weight="bold"), textvariable=self.text.MANAGEMENT)
        self.settings_label.grid(row=1, column=0, padx=15, pady=(10, 0),  sticky="w")

        self.buttons_frame = ctk.CTkFrame(self.main_frame)
        self.buttons_frame.grid(row=2, column=0, padx=15, pady=(5,10), sticky="nsew")
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)

        self.theme_button = IconButton(
            self.buttons_frame, 
            command=self.open_backcup_popup, 
            text_var=self.text.THEMES, 
            icon_type=IconType.PALLETE,
            font=ctk.CTkFont(size=15),
            height=40
        )
        self.theme_button.grid(row=0, column=0, padx=(10, 5), pady=5,  sticky="nsew")

        self.backup_button = IconButton(
            self.buttons_frame, 
            command=None, 
            text_var=self.text.BACKUP, 
            icon_type=IconType.DISK,
            font=ctk.CTkFont(size=15),
            height=40
        )
        self.backup_button.grid(row=0, column=1, padx=(5, 10), pady=5,  sticky="nsew")

    def build_language(self):
        self.language_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=18, weight="bold"), textvariable=self.text.LANGUAGE)
        self.language_label.grid(row=3, column=0, padx=15, pady=(10, 0),  sticky="w")

        self.language_btns = SmartScrollableFrame(self.main_frame, height=SCROLLABLE_FRAME_SIZE)
        self.language_btns.grid(row=4, column=0, padx=15, pady=(5,10), sticky="nsew")
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
        self.option_frame.grid(row=0, column=0, padx=0, pady=10, sticky="nsew")
        self.option_frame.grid_columnconfigure(1, weight=1)

        self.option_label = ctk.CTkLabel(self.option_frame, font=ctk.CTkFont(size=18, weight="bold"), textvariable=self.text.OPTION_SWITCH)
        self.option_label.grid(row=0, column=0, padx=(15, 0), pady=5,  sticky="w")

        self.option_switch = ctk.CTkSwitch(self.option_frame, progress_color=PRIMARY_THEME.fg_color(), text="", command=ThemeJSON.toggle_new_year_popup_status, cursor='hand2', switch_height=25, switch_width=50)
        self.option_switch.grid(row=0, column=1, padx=20, pady=5,  sticky="w")
        
        if ThemeJSON.is_new_year_popup_hidden():
            self.option_switch.select()

    def open_theme_popup(self):
        if self.popup_frame is not None:
            self.popup_frame.destroy()

        from . import PopupHandler
        self.popup_frame = PopupHandler.theme_popup(
            self, 
            on_color_change=self.change_color,
            on_theme_change=self.on_theme_change
        )

    def open_backcup_popup(self):
        if self.popup_frame is not None:
            self.popup_frame.destroy()

        from . import PopupHandler
        self.popup_frame = PopupHandler.theme_popup(
            self, 
            on_color_change=self.change_color,
            on_theme_change=self.on_theme_change
        )

    def change_language(self, language):
        ThemeJSON.save_current_language(language)
        self.on_language_change()
        self.text.reload_language()

        self.back_button.configure(text=i18n.t('actions.back'))

        current_lang = ThemeJSON.get_current_language()
        for lang, btn in self.language_dict.items():
            btn.main_color = current_lang == lang 
            btn.reload_colors()

            if current_lang == lang:
                self.selected_lang_btn = btn

    def change_color(self):
        self.back_button.reload_colors()
        self.option_switch.configure(progress_color=PRIMARY_THEME.fg_color())
        
        self.selected_lang_btn.reload_colors()
        self.on_color_change()

    def build_back_button(self):
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=9, column=0, padx=10, pady=10, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)

        self.back_button = CustomButton(self.button_frame, text=i18n.t('actions.back'), command=self.destroy, font_size=15, height=40)
        self.back_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.build_buttons()
        self.build_language()
        self.build_new_year_options()
        self.build_back_button()

    class _Theme_Texts:
        def __init__(self):
            self.LANGUAGE = ctk.StringVar(value=i18n.t('settings.language'))
            self.OPTION_SWITCH = ctk.StringVar(value=i18n.t('settings.option_switch'))
            self.MANAGEMENT = ctk.StringVar(value=i18n.t('settings.management'))
            self.THEMES = ctk.StringVar(value=i18n.t('settings.themes'))
            self.BACKUP = ctk.StringVar(value=i18n.t('settings.backup'))

        def reload_language(self):
            self.LANGUAGE.set(i18n.t('settings.language'))
            self.OPTION_SWITCH.set(i18n.t('settings.option_switch'))
            self.MANAGEMENT.set(i18n.t('settings.management'))
            self.THEMES.set(i18n.t('settings.themes'))
            self.BACKUP.set(i18n.t('settings.backup'))