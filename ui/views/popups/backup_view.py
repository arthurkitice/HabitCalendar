import customtkinter as ctk
from ui.widgets import CustomButton, IconButton, PopupFrame
from icon_assets import DISK, CALENDAR_REFRESH, EXPORT, IMPORT
from themes import PRIMARY_THEME, TEXT_COLOR
from backup_manager import create_backup, restore_backup, get_backup_info, export_database, import_database
import i18n, platform, subprocess
from datetime import datetime, timedelta
from functools import partial

DEFAULT_COLOR = 'pink-man'
SCROLLABLE_FRAME_SIZE = 85

class BackupView(PopupFrame):
    def __init__(self, parent, on_restore_backup):
        super().__init__(parent)

        self.parent = parent
        self.on_restore_backup = on_restore_backup
        self.popup_frame = None

        self.buttons_config = {
            "font":ctk.CTkFont(size=15),
            "height":30,
            "width":125
        }

        self.text = self._Theme_Texts()

        self.build_ui()

    # --- Métodos de construção ---

    def build_button_row_1(self):
        self.save_restore_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=18, weight="bold"), text=self.text.TITLE_SAVE_RESTORE)
        self.save_restore_label.grid(row=0, column=0, padx=15, pady=(10, 0),  sticky="w")

        # Formata o timestamp real do arquivo com o formato pego acima
        date_format = self._get_correct_time_format()

        text = f"{self.text.LAST_BACKUP} {date_format}"

        self.backup_time = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=16), text=text)
        self.backup_time.grid(row=1, column=0, padx=15, pady=0,  sticky="w")

        self.save_restore_btns_frame = ctk.CTkFrame(self.main_frame)
        self.save_restore_btns_frame.grid(row=2, column=0, padx=15, pady=(5,10), sticky="nsew")
        self.save_restore_btns_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.buttons_config["parent"] = self.save_restore_btns_frame

        fg, hover = PRIMARY_THEME.get_colors()
        self.save_button = IconButton(command=self._show_save_popup, text=self.text.SAVE, icon=DISK, fg_color=fg, hover_color=hover, **self.buttons_config)
        self.save_button.grid(row=0, column=0, padx=(10, 5), pady=5,  sticky="nsew")

        self.restore_button = IconButton(command=self._show_restore_popup, text=self.text.RESTORE, icon=CALENDAR_REFRESH, **self.buttons_config)
        self.restore_button.grid(row=0, column=1, padx=(5, 10), pady=5,  sticky="nsew")

        self.backup_info_1 = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=15), text=self.text.BACKUP_INFO, text_color='grey')
        self.backup_info_1.grid(row=3, column=0, padx=15, pady=2,  sticky="nsew")

    def build_button_row_2(self):
        self.import_export_label = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=18, weight="bold"), text=self.text.TITLE_IMPORT_EXPORT)
        self.import_export_label.grid(row=4, column=0, padx=15, pady=(20, 0),  sticky="w")

        self.import_export_btns_frame = ctk.CTkFrame(self.main_frame)
        self.import_export_btns_frame.grid(row=5, column=0, padx=15, pady=(5,10), sticky="nsew")
        self.import_export_btns_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.buttons_config["parent"] = self.import_export_btns_frame

        fg, hover = PRIMARY_THEME.get_colors()
        self.export_button = IconButton(command=self.button_export_click, text=self.text.EXPORT, icon=EXPORT, fg_color=fg, hover_color=hover, **self.buttons_config)
        self.export_button.grid(padx=(10, 5), pady=5,  sticky="nsew")

        self.import_button = IconButton(command=self.button_import_click, text=self.text.IMPORT, icon=IMPORT, **self.buttons_config)
        self.import_button.grid(row=0, column=1, padx=(5, 10), pady=5,  sticky="nsew")

        self.backup_info_2 = ctk.CTkLabel(self.main_frame, font=ctk.CTkFont(size=15), text=self.text.EXPORT_INFO, text_color='grey')
        self.backup_info_2.grid(row=6, column=0, padx=15, pady=(2, 15),  sticky="nsew")

    def build_ui(self):
        self.build_button_row_1()
        self.build_button_row_2()
        self.build_back_button()

    def on_save_backup(self):
        create_backup()
        date_format = self._get_correct_time_format()
        text = f"{self.text.LAST_BACKUP} {date_format}"
        self.backup_time.configure(text=text)

    # --- Métodos que chamam callback ---

    def on_restore(self):
        restore_backup()
        self.on_restore_backup()

    def on_import(self, file_path):
        import_database(file_path)
        self.on_restore_backup()
    
    # --- Métodos chamados por botões e popups ---

    def button_export_click(self):
        file_path = DialogHelper.ask_save_file(
            title="Export Backup",
            defaultextension=".habitbackup",
            filetypes=[("Backup Habit Calendar", "*.habitbackup"), ("Todos os arquivos", "*.*")],
            initialfile="my_habit_backup"
        )

        if file_path:
            export_database(file_path)

    def button_import_click(self):
        file_path = DialogHelper.ask_open_file(
            title="Import Backup",
            filetypes=[("Backup Habit Calendar", "*.habitbackup")]
        )

        if file_path:
            self._show_import_popup(file_path)

    def _show_save_popup(self):
        from .popup_handler import save_backup_popup
        self.popup_frame = save_backup_popup(self, on_save=self.on_save_backup)

    def _show_restore_popup(self):
        from .popup_handler import restore_backup_popup
        self.popup_frame = restore_backup_popup(self, on_save=self.on_restore)

    def _show_import_popup(self, file_path):
        from .popup_handler import import_popup
        self.popup_frame = import_popup(self, on_save=partial(self.on_import, file_path))

    # --- Utilitários ---

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

# --- Classe helper para lidar com a diferença entre sistemas ---

class DialogHelper:
    @staticmethod
    def ask_save_file(title: str, initialfile: str, filetypes: list, defaultextension: str) -> str:
        if platform.system() == "Linux":
            try:
                process = subprocess.run(
                    [
                        'zenity', '--file-selection', '--save', '--confirm-overwrite',
                        f'--title={title}',
                        f'--filename={initialfile}{defaultextension}',
                        '--file-filter=*.habitbackup'
                    ],
                    capture_output=True, text=True
                )
                if process.returncode == 0:
                    return process.stdout.strip()
                return ""
            except FileNotFoundError:
                pass
        
        # Windows, macOS ou fallback de emergência para Linux
        return ctk.filedialog.asksaveasfilename(
            title=title,
            initialfile=initialfile,
            filetypes=filetypes,
            defaultextension=defaultextension
        )

    @staticmethod
    def ask_open_file(title: str, filetypes: list) -> str:
        if platform.system() == "Linux":
            try:
                process = subprocess.run(
                    [
                        'zenity', '--file-selection', 
                        f'--title={title}', 
                        '--file-filter=*.habitbackup'
                    ],
                    capture_output=True, text=True
                )
                if process.returncode == 0:
                    return process.stdout.strip()
                return ""
            except FileNotFoundError:
                pass
        
        return ctk.filedialog.askopenfilename(title=title, filetypes=filetypes)