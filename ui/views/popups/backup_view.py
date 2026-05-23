import customtkinter as ctk
from ui.widgets import CustomButton, IconButton
from icon_assets import DISK, CALENDAR_REFRESH, EXPORT, IMPORT
from themes import PRIMARY_THEME, TEXT_COLOR
from database_manager import create_backup, restore_backup, get_backup_info
import i18n
from datetime import datetime, timedelta

DEFAULT_COLOR = 'pink-man'
SCROLLABLE_FRAME_SIZE = 85

class BackupView(ctk.CTkFrame):
    def __init__(self, parent, on_restore_backup):
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
        self.on_restore_backup = on_restore_backup
        self.popup_frame = None

        self.text = self._Theme_Texts()

        self.build_ui()

    def build_button_row_1(self):
        self.settings_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=18, weight="bold"), text=self.text.TITLE_SAVE_RESTORE)
        self.settings_label.grid(padx=15, pady=(10, 0),  sticky="w")

        # Formata o timestamp real do arquivo com o formato pego acima
        data_formatada = self._get_correct_time_format()

        # Junta a label "Último backup:" com a data já formatada
        text = f"{self.text.LAST_BACKUP} {data_formatada}"

        self.backup_time = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=16), text=text)
        self.backup_time.grid(padx=15, pady=0,  sticky="w")

        self.buttons_frame = ctk.CTkFrame(self.main_frame)
        self.buttons_frame.grid(padx=15, pady=(5,10), sticky="nsew")
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        buttons_config = {
            "parent":self.buttons_frame,
            "font":ctk.CTkFont(size=15),
            "height":30,
            "width":125
        }

        self.backup_button = IconButton(command=self.on_save_backup, text=self.text.SAVE, icon=DISK, fg_color=PRIMARY_THEME.fg_color(), **buttons_config)
        self.backup_button.grid(row=0, column=0, padx=(10, 5), pady=5,  sticky="nsew")

        self.backup_button = IconButton(command=self.on_restore, text=self.text.RESTORE, icon=CALENDAR_REFRESH, **buttons_config)
        self.backup_button.grid(row=0, column=1, padx=(5, 10), pady=5,  sticky="nsew")

        self.backup_info = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=15), text=self.text.BACKUP_INFO, text_color='grey')
        self.backup_info.grid(padx=15, pady=2,  sticky="nsew")

    def build_button_row_2(self):
        self.settings_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=18, weight="bold"), text=self.text.TITLE_IMPORT_EXPORT)
        self.settings_label.grid(padx=15, pady=(20, 0),  sticky="w")

        self.buttons_frame = ctk.CTkFrame(self.main_frame)
        self.buttons_frame.grid(padx=15, pady=(5,10), sticky="nsew")
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        buttons_config = {
            "parent":self.buttons_frame,
            "font":ctk.CTkFont(size=15),
            "height":30,
            "width":125
        }

        self.backup_button = IconButton(command=None, text=self.text.EXPORT, icon=EXPORT, fg_color=PRIMARY_THEME.fg_color(), **buttons_config)
        self.backup_button.grid(padx=(10, 5), pady=5,  sticky="nsew")

        self.backup_button = IconButton(command=None, text=self.text.IMPORT, icon=IMPORT, **buttons_config)
        self.backup_button.grid(row=0, column=1, padx=(5, 10), pady=5,  sticky="nsew")

        text='Você pode gerar uma cópia do banco de dados\nque ficará salva no seu computador ou pen drive.'
        self.backup_info = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=15), text=self.text.EXPORT_INFO, text_color='grey')
        self.backup_info.grid(padx=15, pady=2,  sticky="nsew")

    def build_back_button(self):
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(padx=10, pady=(20,10), sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)

        self.back_button = CustomButton(self.button_frame, text=i18n.t('actions.back'), command=self.destroy, font_size=15, height=40)
        self.back_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def on_save_backup(self):
        create_backup()
        data_formatada = self._get_correct_time_format()
        text = f"{self.text.LAST_BACKUP} {data_formatada}"
        self.backup_time.configure(text=text)

    def on_restore(self):
        restore_backup()
        self.on_restore_backup()

    def _get_correct_time_format(self):
        timestamp = get_backup_info()

        if timestamp:
            backup_date = datetime.fromtimestamp(timestamp)
            today_date = datetime.now().date()
            if backup_date.date() == today_date:
                formato_hora = self.text.TODAY_TIME
            elif backup_date.date() == today_date - timedelta(days=1):
                formato_hora = self.text.YESTERDAY_TIME
            else:
                formato_hora = self.text.TIME
            return backup_date.strftime(formato_hora)
        else:
            return self.text.NO_BACKUP

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.build_button_row_1()
        self.build_button_row_2()
        self.build_back_button()

    class _Theme_Texts:
        def __init__(self):
            self.TIME = i18n.t('backup.time')
            self.TODAY_TIME = i18n.t('backup.today_time')
            self.YESTERDAY_TIME = i18n.t('backup.yesterday_time')
            self.LAST_BACKUP = i18n.t('backup.last_backup')
            self.SAVE = i18n.t('backup.save')
            self.RESTORE = i18n.t('backup.restore')
            self.EXPORT = i18n.t('backup.export')
            self.IMPORT = i18n.t('backup.import')
            self.TITLE_SAVE_RESTORE = i18n.t('backup.title_save_restore')
            self.TITLE_IMPORT_EXPORT = i18n.t('backup.title_import_export')
            self.BACKUP_INFO = i18n.t('backup.backup_info')
            self.EXPORT_INFO = i18n.t('backup.export_info')
            self.NO_BACKUP = i18n.t('backup.no_backup')

