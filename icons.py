from customtkinter import CTkImage
from enum import Enum, auto
import cairosvg
import io
from PIL import Image

def carregar_icone_svg(nome_arquivo, tamanho_icone):
    # Multiplicamos o tamanho desejado por 4 para garantir nitidez 
    largura_render = tamanho_icone[0] * 4
    altura_render = tamanho_icone[1] * 4

    imagem_pillow = {}
    for i in ['dark', 'light']:
        png_bytes = cairosvg.svg2png(
            url=f"ui/icons/{i}/{nome_arquivo}.svg", 
            output_width=largura_render, 
            output_height=altura_render
        )
        
        imagem_memoria = io.BytesIO(png_bytes)
        imagem_pillow[i] = Image.open(imagem_memoria)
    
    return CTkImage(light_image=imagem_pillow['light'], dark_image=imagem_pillow['dark'], size=tamanho_icone)

class IconImages:
    LEFT_ARROW = carregar_icone_svg("left_arrow", (30, 30))
    RIGHT_ARROW = carregar_icone_svg("right_arrow", (30, 30))
    PLUS = carregar_icone_svg("plus", (30, 30))
    EDIT = carregar_icone_svg("pencil", (30, 30))
    TRASH = carregar_icone_svg("bin", (30, 30))
    CONFIG = carregar_icone_svg("settings", (30, 30))
    PALLETE = carregar_icone_svg("pallete", (20, 20))
    BIG_TRASH = carregar_icone_svg("bin", (40, 40))

class Direction(Enum):
    PREV = auto()
    NEXT = auto()

class IconType(Enum):
    EDIT = auto()
    REMOVE = auto()
    CONFIG = auto()
    PALLETE = auto()
    PLUS = auto()
    BIG_TRASH = auto()

ARROWS = {
    Direction.NEXT: IconImages.RIGHT_ARROW, 
    Direction.PREV: IconImages.LEFT_ARROW
}

ICONS = {
    IconType.EDIT: IconImages.EDIT,
    IconType.REMOVE: IconImages.TRASH,
    IconType.CONFIG: IconImages.CONFIG,
    IconType.PALLETE: IconImages.PALLETE,
    IconType.PLUS: IconImages.PLUS,
    IconType.BIG_TRASH: IconImages.BIG_TRASH
}