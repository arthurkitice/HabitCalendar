import customtkinter as ctk
from ui.widgets import CustomButton, IconButton
from icon_assets import DISK, CALENDAR_REFRESH, EXPORT, IMPORT
from themes import PRIMARY_THEME, TEXT_COLOR
from database_manager import create_backup, restore_backup, get_backup_info, export_database, import_database
import i18n, platform, subprocess
from datetime import datetime, timedelta
from functools import partial

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

        fg, hover = PRIMARY_THEME.get_colors()
        self.backup_button = IconButton(command=self._show_save_popup, text=self.text.SAVE, icon=DISK, fg_color=fg, hover_color=hover, **buttons_config)
        self.backup_button.grid(row=0, column=0, padx=(10, 5), pady=5,  sticky="nsew")

        self.backup_button = IconButton(command=self._show_restore_popup, text=self.text.RESTORE, icon=CALENDAR_REFRESH, **buttons_config)
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

        fg, hover = PRIMARY_THEME.get_colors()
        self.backup_button = IconButton(command=self.button_export_click, text=self.text.EXPORT, icon=EXPORT, fg_color=fg, hover_color=hover, **buttons_config)
        self.backup_button.grid(padx=(10, 5), pady=5,  sticky="nsew")

        self.backup_button = IconButton(command=self.button_import_click, text=self.text.IMPORT, icon=IMPORT, **buttons_config)
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

    def on_import(self, file_path):
        import_database(file_path)
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

    def _show_save_popup(self):
        from .popup_handler import save_backup_popup
        self.popup_frame = save_backup_popup(self, on_save=self.on_save_backup)

    def _show_restore_popup(self):
        from .popup_handler import restore_backup_popup
        self.popup_frame = restore_backup_popup(self, on_save=self.on_restore)

    def _show_import_popup(self, file_path):
        from .popup_handler import import_popup
        self.popup_frame = import_popup(self, on_save=partial(self.on_import, file_path))

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.build_button_row_1()
        self.build_button_row_2()
        self.build_back_button()

    def button_export_click(self):
        # Abre a janela para o usuário escolher a pasta e o nome do arquivo
        caminho_destino = DialogHelper.ask_save_file(
            title="Exportar Backup",
            defaultextension=".habitbackup",
            filetypes=[("Backup HabitCalendar", "*.habitbackup"), ("Todos os arquivos", "*.*")],
            initialfile="meu_backup_habitos" # Nome sugerido que aparece preenchido
        )

        # Se o usuário fechar a janela ou clicar em Cancelar, retorna vazio ("")
        if caminho_destino:
            # Aqui você chama aquela função de exportar passando o caminho_destino
            sucesso = export_database(caminho_destino)
            if sucesso:
                print("Exportado com sucesso!")

    def button_import_click(self):
        # Abre a janela pedindo para ele selecionar um arquivo existente
        caminho_arquivo = DialogHelper.ask_open_file(
            title="Importar Backup",
            filetypes=[("Backup HabitCalendar", "*.habitbackup")]
        )

        # Se ele selecionou um arquivo e não cancelou
        if caminho_arquivo:
            self._show_import_popup(caminho_arquivo)

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

class DialogHelper:
    @staticmethod
    def ask_save_file(title: str, initialfile: str, filetypes: list, defaultextension: str) -> str:
        if platform.system() == "Linux":
            try:
                # Chama o Zenity para gerar a janela GTK nativa no Linux
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
                return "" # O utilizador cancelou a janela
            except FileNotFoundError:
                pass # Se o Zenity não estiver instalado (raro), avança para o fallback do Tkinter
        
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
                return "" # O utilizador cancelou a janela
            except FileNotFoundError:
                pass
        
        return ctk.filedialog.askopenfilename(title=title, filetypes=filetypes)