import customtkinter as ctk

class AlterTrackerWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_save, tracker_name=None, tracker_id=None):
        super().__init__(parent)
        self.geometry("400x300")
        self.title("Adicionar Novo Marcador")

        self.on_save = on_save
        self.tracker_id = tracker_id
        self.tracker_name = tracker_name
        # Garante que a janela fique na frente da principal
        self.attributes("-topmost", True)

        self.build_ui()
        

    def ui_new_tracker(self):
        self.label = ctk.CTkLabel(self, text=f"Novo Marcador:")
        self.label.pack(padx=20, pady=20)

        self.entry = ctk.CTkEntry(self, placeholder_text="Digite o nome do marcador")
        self.entry.pack(padx=20, pady=10)

        self.btn_confirm = ctk.CTkButton(self, text="Salvar", command=self.save)
        self.btn_confirm.pack(padx=20, pady=20)

    def ui_edit_tracker(self, tracker_name):
        self.label = ctk.CTkLabel(self, text=f"Editar Marcador '{tracker_name}':")
        self.label.pack(padx=20, pady=20)

        self.entry = ctk.CTkEntry(self, placeholder_text="Digite o novo nome do marcador")
        self.entry.pack(padx=20, pady=10)

        self.entry.insert(0, tracker_name)

        self.btn_confirm = ctk.CTkButton(self, text="Salvar", command=self.save)
        self.btn_confirm.pack(padx=20, pady=20)

    def build_ui(self):
        if self.tracker_name:
            self.ui_edit_tracker(self.tracker_name)
        else:
            self.ui_new_tracker()

    def back(self):
        self.destroy()

    def save(self):
        if self.tracker_id is not None:
            # Editar marcador existente
            self.on_save(self.entry.get(), self.tracker_id)
        else:
            self.on_save(self.entry.get())
        self.back()