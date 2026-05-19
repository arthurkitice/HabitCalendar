from ui.views.main_app.app import CalendarApp
from constants import LANGUAGES
from config import ThemeJSON
import i18n
import os
import locale

def detectar_idioma_sistema() -> str:
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

if __name__ == "__main__":
    if ThemeJSON.get_current_language() == None:
        ThemeJSON.save_current_language(detectar_idioma_sistema())

    base_dir = os.path.dirname(os.path.abspath(__file__))
    i18n.load_path.append(os.path.join(base_dir, 'locales'))

    i18n.set('filename_format', '{locale}.{format}')

    # 3. Define o idioma atual (pode puxar de um arquivo de config depois)
    i18n.set('locale', ThemeJSON.get_current_language())

    # 4. Opcional: Se faltar tradução em PT, ele tenta buscar no EN
    i18n.set('fallback', 'en')

    app = CalendarApp()
    app.mainloop()