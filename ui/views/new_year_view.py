import customtkinter as ctk
from ui.widgets import style_button
from constants import AuxColorGreen

class NewYearView(ctk.CTkFrame):
    def __init__(self, parent, on_save, year):
        super().__init__(
            parent, 
            width=500, 
            height=400, 
            corner_radius=15, 
            border_width=1, 
            border_color="white",
            fg_color="#2B2B2B"
        )

        self.grid_propagate(False)

        self.parent = parent
        self.on_save = on_save
        self.year = year
        self.build_ui()

    def ui(self):
        
        self.label = ctk.CTkLabel(self, text=f"Novo Ano: {self.year}\n", font=ctk.CTkFont(size=22, weight="bold"))
        self.label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.label = ctk.CTkLabel(self, text=f"Confirmar criação do ano?\nEssa ação aumentará o\ntamanho do banco de dados\n", font=ctk.CTkFont(size=16), text_color="grey")
        self.label.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent", width=500)
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid(row=3, column=1)

        self.btn_return = style_button(self.button_frame, text="Cancelar", font=ctk.CTkFont(size=15, weight="bold"), command=self.destroy, height=35, width=250)
        self.btn_return.grid(row=0, column=0, padx=5, pady=10)

        self.btn_confirm = style_button(self.button_frame, text="Confirmar", font=ctk.CTkFont(size=15, weight="bold"), command=self.save, height=35, width=250, fg_color=AuxColorGreen.FG, hover_color=AuxColorGreen.HOVER)
        self.btn_confirm.grid(row=0, column=1, padx=5, pady=10)

    def build_ui(self):
        self.grid_columnconfigure((0, 2), weight=1, uniform="main")
        self.grid_columnconfigure(1, weight=2, uniform="main")
        self.grid_rowconfigure((0, 5), weight=1, uniform="main")

        self.ui()

    def save(self):
        self.on_save()
        self.destroy()