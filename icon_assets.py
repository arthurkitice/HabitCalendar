from customtkinter import CTkImage
import cairosvg
import io
from PIL import Image
from constants import BASE_DIR
import os

def _carregar_icone_svg(nome_arquivo, tamanho_icone):
    largura_render = tamanho_icone[0] * 4
    altura_render = tamanho_icone[1] * 4

    imagem_pillow = {}
    for i in ['dark', 'light']:
        caminho = os.path.join(BASE_DIR, 'ui', 'icons', i, f'{nome_arquivo}.svg')
        
        # 1. Abre o arquivo e lê os bytes puros
        with open(caminho, 'rb') as f:
            svg_bytes = f.read()

        # 2. Usa 'bytestring' em vez de 'url'
        png_bytes = cairosvg.svg2png(
            bytestring=svg_bytes, 
            output_width=largura_render,
            output_height=altura_render
        )
        
        imagem_memoria = io.BytesIO(png_bytes)
        imagem_pillow[i] = Image.open(imagem_memoria)
    
    return CTkImage(light_image=imagem_pillow['light'], dark_image=imagem_pillow['dark'], size=tamanho_icone)

LEFT_ARROW: CTkImage = _carregar_icone_svg("left_arrow", (30, 30))
RIGHT_ARROW: CTkImage = _carregar_icone_svg("right_arrow", (30, 30))
PLUS: CTkImage = _carregar_icone_svg("plus", (30, 30))
EDIT: CTkImage = _carregar_icone_svg("pencil", (30, 30))
TRASH: CTkImage = _carregar_icone_svg("bin", (30, 30))
CONFIG: CTkImage = _carregar_icone_svg("settings", (30, 30))
PALLETE: CTkImage = _carregar_icone_svg("pallete", (20, 20))
BIG_TRASH: CTkImage = _carregar_icone_svg("bin", (40, 40))
SETTINGS: CTkImage = _carregar_icone_svg("slide_settings", (20, 20))
DISK: CTkImage = _carregar_icone_svg("disk", (20, 20))
CALENDAR_REFRESH: CTkImage = _carregar_icone_svg("calendar_refresh", (20, 20))
IMPORT: CTkImage = _carregar_icone_svg("import", (20, 20))
EXPORT: CTkImage = _carregar_icone_svg("export", (20, 20))