import customtkinter as ctk

def get_navigation_button_style(self, direction, disabled=False):
        direction_text = "<" if direction == "prev" else ">"
        direction_condition = self.current_month_index > 0 if direction == "prev" else self.current_month_index < len(self.months) - 1

        if disabled or not direction_condition:
            return {
                "text": " ", # Mantém a sua sacada genial da geometria
                "fg_color": "transparent", # O botão fica invisível
                "hover_color": "gray", # Evita que fique cinza ao passar o mouse
                "text_color": "gray",
                "text_color_disabled": "gray",
                "state": "disabled",
                "cursor": "arrow" # Cursor normal para indicar que não é clicável
            }
        else:
            return {
                "text": direction_text, # Exibe a seta apenas se for possível navegar
                "fg_color": "#2F0C6F", # Verde moderno ou Cinza escuro
                "hover_color": "#280A5F", # Mantém a cor no hover
                "text_color": "white", # Evita a piscada preta
                "text_color_disabled": "gray", # Caso desabilite um dia válido no futuro
                "state": "normal",
                "cursor": "hand2" # Muda o cursor para indicar que é clicável
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
                "fg_color": "#227651" if day.checked else "#333333", # Verde moderno ou Cinza escuro
                "hover_color": "#1A593D" if day.checked else "#282828", # Mantém a cor no hover
                "text_color": "white", # Evita a piscada preta
                "text_color_disabled": "gray", # Caso desabilite um dia válido no futuro
                "state": "normal",
                "cursor": "hand2" # Muda o cursor para indicar que é clicável
            }
        
def build_day_button(self, day, row, column):
        style = get_button_style(self, day)

        button = ctk.CTkButton(
            self.days_frame, 
            corner_radius=20, 
            text=style["text"], 
            command=lambda d_id=day.id, r=row, c=column: self.check_day(d_id, r, c),
            fg_color=style["fg_color"],
            state=style["state"],
            text_color=style["text_color"],
            text_color_disabled=style["text_color_disabled"],
            hover_color=style["hover_color"],
            cursor=style["cursor"]
        )
        #button.grid(row=row, column=column, padx=5, pady=5, sticky="nsew") -> Adicionar na view depois

        return button

def build_navigation_button(self, direction):
    style = get_navigation_button_style(self, direction)

    button = ctk.CTkButton(
        self.top_frame, 
        text=style["text"], 
        command=lambda: self.change_month(opperation=direction), 
        state=style["state"],
        fg_color=style["fg_color"],
        text_color=style["text_color"],
        text_color_disabled=style["text_color_disabled"],
        hover_color=style["hover_color"],
        cursor=style["cursor"]
    )
    return button
    #self.prev_button.grid(row=0, column=0, padx=5, pady=5, sticky="w") -> Adicionar na view depois

def update_day_button(self, button, day, key, clickable=True, **kwargs):
    style = get_button_style(self, day, clickable)

    config = {
        "text":style["text"],
        "command":lambda d_id=day.id, r=key[0], c=key[1]: self.check_day(d_id, r, c),
        "fg_color":style["fg_color"],
        "state":style["state"],
        "text_color":style["text_color"],
        "text_color_disabled":style["text_color_disabled"],
        "hover_color":style["hover_color"],
        "cursor":style["cursor"],
        **kwargs
    }

    button.configure(**config)

def update_navigation_button(self, button, direction, disabled=False, **kwargs):
    style = get_navigation_button_style(self, direction, disabled=disabled)

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