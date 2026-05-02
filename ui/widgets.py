import customtkinter as ctk
from PIL import Image
from constants import Direction
import cairosvg
import io

def carregar_icone_svg(caminho_arquivo, tamanho_icone):
    # Multiplicamos o tamanho desejado por 4 para garantir nitidez 
    largura_render = tamanho_icone[0] * 4
    altura_render = tamanho_icone[1] * 4

    png_bytes = cairosvg.svg2png(
        url=caminho_arquivo, 
        output_width=largura_render, 
        output_height=altura_render
    )
    
    imagem_memoria = io.BytesIO(png_bytes)
    imagem_pillow = Image.open(imagem_memoria)
    
    return ctk.CTkImage(light_image=imagem_pillow, dark_image=imagem_pillow, size=tamanho_icone)

left_arrow_icon = carregar_icone_svg("ui/icons/left_arrow_dark.svg", (30, 30))
right_arrow_icon = carregar_icone_svg("ui/icons/right_arrow_dark.svg", (30, 30))
plus_icon = carregar_icone_svg("ui/icons/plus_dark.svg", (30, 30))
edit_icon = carregar_icone_svg("ui/icons/pencil_dark.svg", (30, 30))
trash_icon = carregar_icone_svg("ui/icons/bin_dark.svg", (30, 30))

def get_navigation_button_style(self, direction):
        direction_condition = self.current_month_index > 0 if direction == Direction.PREV else self.current_month_index < len(self.months) - 1

        if not direction_condition:
            image = plus_icon
        else:
            image = left_arrow_icon if direction == Direction.PREV else right_arrow_icon

        return {
            "text": "",
            "fg_color": "transparent",
            "hover_color": "#272727",
            "text_color": "white",
            "text_color_disabled": "gray",
            "state": "normal",
            "cursor": "hand2",
            "image": image
        }

def get_year_nav_button_style(self, direction):
        direction_condition = self.year - 1 in self.years if direction == Direction.PREV else self.year + 1 in self.years

        if not direction_condition:
            image = plus_icon
        else:
            image = left_arrow_icon if direction == Direction.PREV else right_arrow_icon

        return {
            "text": "",
            "fg_color": "transparent",
            "hover_color": "#272727",
            "text_color": "white",
            "text_color_disabled": "gray",
            "state": "normal",
            "cursor": "hand2",
            "image": image
        }
        
def get_button_style(self, day, clickable=True):
        # Um método auxiliar para limpar o código visual
        if day.number == 0 or not clickable:
            return {
                "text": str(day.number) if day.number != 0 else " ", # Mantém a sua sacada genial da geometria
                "fg_color": "#2F2F2F", # O botão fica invisível
                "hover_color": "gray", # Evita que fique cinza ao passar o mouse
                "text_color": "gray",
                "text_color_disabled": "gray",
                "state": "disabled",
                "cursor": "arrow" # Cursor normal para indicar que não é clicável
            }
        else:
            return {
                "text": str(day.number),
                "fg_color": "#1A593D" if day.checked else "#333333", # Verde moderno ou Cinza escuro
                "hover_color": "#14462F" if day.checked else "#282828", # Mantém a cor no hover
                "text_color": "white", # Evita a piscada preta
                "text_color_disabled": "gray", # Caso desabilite um dia válido no futuro
                "state": "normal",
                "cursor": "hand2" # Muda o cursor para indicar que é clicável
            }

def style_button(frame, text, command, **kwargs):
      button = ctk.CTkButton(
            frame,
            corner_radius=5,
            text=text,
            command=command,
            fg_color= "#333333",
            hover_color= "#282828",
            text_color="white",
            cursor="hand2"
      )

      button.configure(**kwargs)

      return button

def build_day_button(self, day, command):
        style = get_button_style(self, day)

        button = ctk.CTkButton(
            self.days_frame, 
            corner_radius=20, 
            text=style["text"], 
            command=command,
            fg_color=style["fg_color"],
            state=style["state"],
            text_color=style["text_color"],
            text_color_disabled=style["text_color_disabled"],
            hover_color=style["hover_color"],
            cursor=style["cursor"]
        )

        return button

def build_navigation_button(self, direction, command):
    style = get_navigation_button_style(self, direction)

    button = ctk.CTkButton(
        self.top_frame, 
        text=style["text"], 
        command=command, 
        state=style["state"],
        fg_color=style["fg_color"],
        text_color=style["text_color"],
        text_color_disabled=style["text_color_disabled"],
        hover_color=style["hover_color"],
        cursor=style["cursor"],
        image=style["image"],
        height=50,
        width=65
    )
    return button

def build_year_nav_button(self, frame, direction, command):
    style = get_year_nav_button_style(self, direction)

    button = ctk.CTkButton(
        frame, 
        text=style["text"], 
        command=command, 
        state=style["state"],
        fg_color=style["fg_color"],
        text_color=style["text_color"],
        text_color_disabled=style["text_color_disabled"],
        hover_color=style["hover_color"],
        cursor=style["cursor"],
        image=style["image"],
        height=50,
        width=65
    )
    return button


def update_day_button(self, button, day, clickable=True, **kwargs):
    style = get_button_style(self, day, clickable)

    config = {
        "text":style["text"],
        "fg_color":style["fg_color"],
        "state":style["state"],
        "text_color":style["text_color"],
        "text_color_disabled":style["text_color_disabled"],
        "hover_color":style["hover_color"],
        "cursor":style["cursor"],
        **kwargs
    }

    button.configure(**config)

def update_navigation_button(self, button, direction, **kwargs):
    style = get_navigation_button_style(self, direction)

    config = {
        "text":style["text"],
        "fg_color":style["fg_color"],
        "state":style["state"],
        "text_color":style["text_color"],
        "text_color_disabled":style["text_color_disabled"],
        "hover_color":style["hover_color"],
        "cursor":style["cursor"],
        "image":style["image"],
        **kwargs
    }

    button.configure(**config)

def update_empty_button(self, button, day, clickable=False, **kwargs):
    style = get_button_style(self, day, clickable)

    config = {
        "text":style["text"],
        "fg_color":style["fg_color"],
        "state":style["state"],
        "text_color":style["text_color"],
        "text_color_disabled":style["text_color_disabled"],
        "hover_color":style["hover_color"],
        "cursor":style["cursor"],
        **kwargs
    }

    button.configure(**config)

def build_sidebar_button(self, text, command, **kwargs):
        button = ctk.CTkButton(
            self.sidebar_buttons_frame, 
            text=text,
            command=command,
            fg_color="#242424",
            text_color="white",
            hover_color="#1E1E1E",
            cursor="hand2",
            height=40,
            **kwargs
        )
        return button

def build_sidebar_edit_button(self, command, **kwargs):
        button = ctk.CTkButton(
            self.sidebar_buttons_frame, 
            text="",
            image=edit_icon,
            command=command,
            fg_color="#242424",
            text_color="white",
            hover_color="#1E1E1E",
            cursor="hand2",
            width=40,
            height=40,
            **kwargs
        )
        return button

def build_sidebar_remove_button(self, command, **kwargs):
        button = ctk.CTkButton(
            self.sidebar_buttons_frame, 
            text="",
            image=trash_icon,
            command=command,
            fg_color="#242424",
            text_color="white",
            hover_color="#1E1E1E",
            cursor="hand2",
            width=40,
            height=40,
            **kwargs
        )
        return button