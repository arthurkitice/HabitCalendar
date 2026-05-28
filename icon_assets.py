from customtkinter import CTkImage
from PIL import Image
from constants import BASE_DIR
import os

def _load_icon(nome_arquivo, tamanho_icone):
    imagem_pillow = {}
    for i in ['dark', 'light']:
        caminho = os.path.join(BASE_DIR, 'ui', 'icons', i, f'{nome_arquivo}.webp')
        imagem_pillow[i] = Image.open(caminho)
    return CTkImage(light_image=imagem_pillow['light'], dark_image=imagem_pillow['dark'], size=tamanho_icone)

LEFT_ARROW: CTkImage = _load_icon("left_arrow", (30, 30))
RIGHT_ARROW: CTkImage = _load_icon("right_arrow", (30, 30))
PLUS: CTkImage = _load_icon("plus", (30, 30))
EDIT: CTkImage = _load_icon("pencil", (30, 30))
TRASH: CTkImage = _load_icon("bin", (30, 30))
CONFIG: CTkImage = _load_icon("settings", (30, 30))
PALLETE: CTkImage = _load_icon("pallete", (20, 20))
BIG_TRASH: CTkImage = _load_icon("bin", (40, 40))
SETTINGS: CTkImage = _load_icon("slide_settings", (20, 20))
DISK: CTkImage = _load_icon("disk", (20, 20))
CALENDAR_REFRESH: CTkImage = _load_icon("calendar_refresh", (20, 20))
IMPORT: CTkImage = _load_icon("import", (20, 20))
EXPORT: CTkImage = _load_icon("export", (20, 20))