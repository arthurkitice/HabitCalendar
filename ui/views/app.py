import customtkinter as ctk
from repositories import DayRepository, MonthRepository
from dtos import DayDTO
from database import get_db
from helper import get_reversed_days

class CalendarApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calendário")
        self.geometry("1100x700")

        self.months = self.get_months()
        self.current_month_index = 0
        self.btn_dict = {}
        self.build_ui()

    def get_months(self):
        try:
            with get_db() as db:
                month_repository = MonthRepository(db)
                months = month_repository.get_all_months()
                return months
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def get_days(self, month_number):
        try:
            with get_db() as db:
                month_repository = MonthRepository(db)
                days = month_repository.get_days_by_month_number(month_number)
                return days
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def check_day(self, day_id, row, column):
        try:
            with get_db() as db:
                day_repository = DayRepository(db)
                day = day_repository.check_day(day_id)
                style = self.get_button_style(day)
                self.btn_dict[(row, column)].configure(fg_color=style["fg_color"], hover_color=style["hover_color"])
        except Exception as e:
            print(f"Erro inesperado: {e}")

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

    def change_month(self, opperation):
        if opperation == "next":
            if self.current_month_index + 1 < len(self.months):
                self.current_month_index += 1
            
        elif opperation == "prev":
            if self.current_month_index - 1 >= 0:
                self.current_month_index -= 1

        self.update_top_bar()
        self.update_days_frame()
    
    def style_empty_buttons(self):
        cont=0
        for btn in self.btn_dict.values():
            if btn.cget("text") != " ":
                break
            cont+=1
        prev_month_days = get_reversed_days(self.months[self.current_month_index - 1].number if self.current_month_index > 0 else 12) 
        filler_number = 0
        for btn in self.btn_dict.values():
            if cont > 0:
                day = prev_month_days[cont-1]
                style = self.get_button_style(DayDTO(id=0, number=day, checked=False, month_id=0), clickable=False)
                btn.configure(
                    text=style["text"],
                    fg_color=style["fg_color"],
                    state=style["state"],
                    text_color=style["text_color"],
                    text_color_disabled=style["text_color_disabled"],
                    hover_color=style["hover_color"],
                    cursor=style["cursor"]
                )
                cont -= 1
            elif btn.cget("text") == " ":
                filler_number += 1
                style = self.get_button_style(DayDTO(id=0, number=filler_number, checked=False, month_id=0), clickable=False)
                btn.configure(
                    text=style["text"],
                    fg_color=style["fg_color"],
                    state=style["state"],
                    text_color=style["text_color"],
                    text_color_disabled=style["text_color_disabled"],
                    hover_color=style["hover_color"],
                    cursor=style["cursor"]
                )
        
    def build_button(self, day, row, column):
        style = self.get_button_style(day)

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
        button.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

        return button

    def update_days_frame(self):
        days = self.get_days(self.months[self.current_month_index].number)
        filler_number = 0

        for key, btn in self.btn_dict.items():
            if days:
                day = days.pop(0)
            else:
                day = DayDTO(id=0, number=filler_number, checked=False, month_id=0)

            style = self.get_button_style(day)
            
            btn.configure(
                text=style["text"],
                command=lambda d_id=day.id, r=key[0], c=key[1]: self.check_day(d_id, r, c),
                fg_color=style["fg_color"],
                state=style["state"],
                text_color=style["text_color"],
                text_color_disabled=style["text_color_disabled"],
                hover_color=style["hover_color"],
                cursor=style["cursor"]
            )
        
        self.style_empty_buttons()

    def build_days_frame(self):
        days = self.get_days(self.months[self.current_month_index].number)
        filler_number = 0
        for i in range(6):
            for j in range(7):
                if days :
                    day = days.pop(0)
                else:
                    day = DayDTO(id=0, number=filler_number, checked=False, month_id=0)

                self.btn_dict[(i, j)] = self.build_button(day, i, j)

        self.style_empty_buttons()

    def update_top_bar(self):
        self.month_label.configure(text=self.months[self.current_month_index].name, text_color="white")

        prev_style = self.get_navigation_button_style("prev")

        self.prev_button.configure(
            text=prev_style["text"],
            state=prev_style["state"],
            fg_color=prev_style["fg_color"],
            text_color=prev_style["text_color"],
            text_color_disabled=prev_style["text_color_disabled"],
            hover_color=prev_style["hover_color"],
            cursor=prev_style["cursor"]
        )

        next_style = self.get_navigation_button_style("next")

        self.next_button.configure(
            text=next_style["text"],
            state=next_style["state"],
            fg_color=next_style["fg_color"],
            text_color=next_style["text_color"],
            text_color_disabled=next_style["text_color_disabled"],
            hover_color=next_style["hover_color"],
            cursor=next_style["cursor"]
        )

    def build_top_bar(self):
        self.month_label = ctk.CTkLabel(
            self.top_frame, 
            text=self.months[self.current_month_index].name, 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        self.month_label.grid(row=0, column=1, padx=5, pady=5)

        prev_style = self.get_navigation_button_style("prev")

        self.prev_button = ctk.CTkButton(
            self.top_frame, 
            text="<" if self.current_month_index > 0 else " ", 
            command=lambda: self.change_month(opperation="prev"), 
            state=prev_style["state"],
            fg_color=prev_style["fg_color"],
            text_color=prev_style["text_color"],
            text_color_disabled=prev_style["text_color_disabled"],
            hover_color=prev_style["hover_color"],
            cursor=prev_style["cursor"]
        )
        self.prev_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        next_style = self.get_navigation_button_style("next")

        self.next_button = ctk.CTkButton(
            self.top_frame, 
            text=next_style["text"], 
            command=lambda: self.change_month(opperation="next"), 
            state=next_style["state"],
            fg_color=next_style["fg_color"],
            text_color=next_style["text_color"],
            text_color_disabled=next_style["text_color_disabled"],
            hover_color=next_style["hover_color"],
            cursor=next_style["cursor"]
        )
        self.next_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    def build_week_days_frame(self):
        week_days = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        for i, day in enumerate(week_days):
            label = ctk.CTkLabel(self.week_days_frame, text=day, font=ctk.CTkFont(size=15, weight="bold"), text_color="white")
            label.grid(row=0, column=i, padx=5, pady=5)

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.top_frame = ctk.CTkFrame(self, corner_radius=0)
        self.top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.top_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="main")
        self.top_frame.grid_rowconfigure(0 , weight=1)

        self.days_frame = ctk.CTkFrame(self, corner_radius=0)
        self.days_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.days_frame.grid_columnconfigure(tuple(range(7)), weight=1, uniform="days")
        self.days_frame.grid_rowconfigure(tuple(range(6)), weight=1, uniform="days")

        self.week_days_frame = ctk.CTkFrame(self, corner_radius=0)
        self.week_days_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew")
        self.week_days_frame.grid_columnconfigure(tuple(range(7)), weight=1, uniform="week_days")
        self.week_days_frame.grid_rowconfigure(0, weight=1)

        self.build_top_bar()
        self.build_days_frame()
        self.build_week_days_frame()