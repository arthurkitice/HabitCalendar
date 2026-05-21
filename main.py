from ui.views.main_app.app import CalendarApp
from constants import LANGUAGES
from config import ThemeJSON
import i18n
import os
import locale
import sys
from database import engine, Base

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

        # Se a sigla estiver nos idiomas que você traduziu, retorna ela
        idiomas_suportados = [key for key in LANGUAGES.keys()]
        if sigla in idiomas_suportados:
            return sigla
        else:
            return 'en' # Fallback para usuários de outros países (ex: França, Japão)
            
    except Exception:
        # Se absolutamente qualquer coisa der errado (ex: SO muito antigo), vai pro Inglês
        return 'en'
    
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