import customtkinter as ctk
from ui.widgets import style_button

class DeleteTrackerView(ctk.CTkFrame):
    def __init__(self, parent, on_save, tracker):
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
        self.tracker = tracker
        self.build_ui()

    def ui(self):
        text_label_1 = f'Tem certeza que deseja\ndeletar o marcador\n"{self.tracker}"?'
        self.label_1 = ctk.CTkLabel(self, text=text_label_1, font=ctk.CTkFont(size=22, weight="bold"))
        self.label_1.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        text_label_2 = f"Você perderá todos os anos\ne marcações associadas.\n\nEssa ação é irreversível.\n"
        self.label_2 = ctk.CTkLabel(self, text=text_label_2, font=ctk.CTkFont(size=16), text_color="grey")
        self.label_2.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent", width=500)
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid(row=3, column=1)

        self.btn_return = style_button(self.button_frame, text="Cancelar", font_size=15, command=self.destroy, height=35, width=250, main_color=False)
        self.btn_return.grid(row=0, column=0, padx=5, pady=10)

        self.btn_confirm = style_button(self.button_frame, text="Confirmar", font_size=15, command=self.save, height=35, width=250)
        self.btn_confirm.grid(row=0, column=1, padx=5, pady=10)

    def build_ui(self):
        self.grid_columnconfigure((0, 2), weight=1, uniform="main")
        self.grid_columnconfigure(1, weight=3, uniform="main")
        self.grid_rowconfigure((0, 5), weight=1, uniform="main")

        self.ui()

    def save(self):
        self.on_save()
        self.destroy()