import customtkinter as ctk
from ui.widgets import style_button

class AlterTrackerFrame(ctk.CTkFrame):
    def __init__(self, parent, on_save, tracker_name=None, tracker_id=None):
        super().__init__(parent, width=500, height=400, corner_radius=15, border_width=4, border_color="black")

        self.grid_propagate(False)

        self.parent = parent
        self.on_save = on_save
        self.tracker_id = tracker_id
        self.tracker_name = tracker_name

        self.build_ui()

    def ui_new_tracker(self):
        self.label = ctk.CTkLabel(self, text=f"Novo Marcador\n", font=ctk.CTkFont(size=22, weight="bold"))
        self.label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.entry = ctk.CTkEntry(self, placeholder_text="Digite o nome do marcador", height=35, width=250)
        self.entry.grid(row=2, column=1, padx=5, pady=5)

    def ui_edit_tracker(self, tracker_name):
        self.label = ctk.CTkLabel(self, text=f"Editar Marcador\n'{tracker_name}'\n", font=ctk.CTkFont(size=22, weight="bold"))
        self.label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.entry = ctk.CTkEntry(self, placeholder_text="Digite o novo nome do marcador", height=35, width=250)
        self.entry.grid(row=2, column=1, padx=5, pady=5)

        self.entry.insert(0, tracker_name)

    def build_ui(self):
        self.grid_columnconfigure((0, 2), weight=1, uniform="main")
        self.grid_columnconfigure(1, weight=2, uniform="main")
        self.grid_rowconfigure((0, 5), weight=1, uniform="main")

        self.btn_confirm = style_button(self, text="Salvar", command=self.save, height=35, width=250)
        self.btn_confirm.grid(row=3, column=1, padx=5, pady=5)

        self.btn_return = style_button(self, text="Cancelar", command=self.back, height=35, width=250)
        self.btn_return.grid(row=4, column=1, padx=5, pady=5)

        if self.tracker_name:
            self.ui_edit_tracker(self.tracker_name)
        else:
            self.ui_new_tracker()

        

    def back(self):
        self.destroy()

    def save(self):
        if self.tracker_id is not None:
            self.on_save(self.entry.get(), self.tracker_id)
        else:
            self.on_save(self.entry.get())
        self.back()