import customtkinter as ctk
from themes import TEXT_COLOR, PRIMARY_THEME
from config import ThemeJSON
from .confirmation_view import ConfirmationView
import i18n

class NewYearView(ConfirmationView):
    def __init__(self, parent, on_save, label, message):
        super().__init__(parent, on_save, label, message)

        self.checkbox()

    def checkbox(self):
        self.check_hide_popup = ctk.CTkCheckBox(
            self, 
            text=f" {i18n.t('new_year.checkbox')}",
            fg_color=PRIMARY_THEME.fg_color(),
            hover_color=PRIMARY_THEME.hover_color(),
            cursor="hand2",
            font=ctk.CTkFont(size=15),
            corner_radius=5,
            border_width=3,
            checkmark_color=TEXT_COLOR
        )
        self.check_hide_popup.grid(row=3, column=1, padx=5, pady=10)

    def save(self):
        if self.check_hide_popup.get() == 1: ThemeJSON.toggle_new_year_popup_status()
        self.on_save()
        self.destroy()