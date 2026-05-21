from ui.views.main_app.app import CalendarApp
from database import engine, Base
from constants import LANGUAGES
from config import ThemeJSON
import logging
import locale
import i18n
import sys
import os

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def detect_sys_language() -> str:
    """
    Detecta o idioma do sistema operacional e retorna a sigla correspondente 
    se for suportada pelo app. Caso contrário, retorna 'en'.
    """
    try:
        # Configura o Python para ler as configurações locais da máquina
        locale.setlocale(locale.LC_ALL, '')
        
        # Pega o idioma do sistema (Exemplo de retorno: ('pt_BR', 'cp1252'))
        idioma_sistema, _ = locale.getlocale()

        # No Mac/Linux, às vezes getlocale() vem vazio, então usamos o os.getenv como plano B
        if not idioma_sistema:
            idioma_sistema = os.getenv('LANG', 'en')

        # Extrai apenas as duas primeiras letras minúsculas (ex: 'pt', 'en', 'es')
        sigla = idioma_sistema[:2].lower()
        
        idiomas_suportados = [key for key in LANGUAGES.keys()]
        if sigla in idiomas_suportados:
            return sigla
        else:
            return 'en'
    except Exception:
        return 'en'

def setup_logging(app_dir: str) -> None:
    log_path = os.path.join(app_dir, 'habitcalendar.log')
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
        ]
    )

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical("Erro não tratado", exc_info=(exc_type, exc_value, exc_traceback))

def gen_icon() -> None:
    icon_path = os.path.join(BASE_DIR, 'icon.png')
    svg_path = os.path.join(BASE_DIR, 'ui/icons/app_icon.svg')
    
    if not os.path.exists(icon_path) and os.path.exists(svg_path):
        import cairosvg
        cairosvg.svg2png(
            url=f"file://{svg_path}",
            output_width=256,
            output_height=256,
            write_to=icon_path
        )

if __name__ == "__main__":
    from database import APP_DIR
    setup_logging(APP_DIR)
    sys.excepthook = handle_exception
    Base.metadata.create_all(bind=engine)
    gen_icon()
        
    if ThemeJSON.get_current_language() == None:
        ThemeJSON.save_current_language(detect_sys_language())

    i18n.load_path.append(os.path.join(BASE_DIR, 'locales'))

    i18n.set('filename_format', '{locale}.{format}')
    i18n.set('locale', ThemeJSON.get_current_language())
    i18n.set('fallback', 'en')

    app = CalendarApp(base_dir=BASE_DIR)
    app.mainloop()