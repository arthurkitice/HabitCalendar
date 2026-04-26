import customtkinter as ctk
from PIL import Image
from constants import Direction

edit_icon = ctk.CTkImage(dark_image=Image.open("ui/icons/edit_icon.png"), size=(30, 30))
trash_icon = ctk.CTkImage(dark_image=Image.open("ui/icons/trash_icon.png"), size=(30, 30))
right_arrow_icon = ctk.CTkImage(dark_image=Image.open("ui/icons/right_arrow_icon.png"), size=(40, 40))
left_arrow_icon = ctk.CTkImage(dark_image=Image.open("ui/icons/left_arrow_icon.png"), size=(40, 40))
plus_icon = ctk.CTkImage(dark_image=Image.open("ui/icons/plus_icon.png"), size=(40, 40))

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
            hover_color= "#303030",
            text_color="white",
            cursor="hand2",
            **kwargs
      )
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