import customtkinter as ctk
from ui.widgets import CustomButton, IconButton
from functools import partial
from constants import IconType
from .delete_year_view import DeleteYearView
from services import YearService

class TrackerFrame(ctk.CTkFrame):
    def __init__(self, parent, tracker_id, tracker_name):
        super().__init__(
            parent, 
            width=500, 
            height=400, 
            corner_radius=15,
            fg_color="#242424",
            border_width=1, 
            border_color="white"
        )

        self.grid_propagate(False)

        self.year_service = YearService()

        self.parent = parent
        self.tracker_id = tracker_id
        self.tracker = tracker_name
        self._update_years()

        self.build_ui()

    def _update_years(self):
        self.years: list[int] = self.year_service.get_years_from_tracker(tracker_id=self.tracker_id)
        self.top_year: int = self.years[-1]
        self.bottom_year: int = self.years[0]

    def remove_year(self, year):
        self.year_service.delete_year(tracker_id=self.tracker_id, year_number=year)
        self._update_years()
        self.top_label.configure(text=f"Marcador: {self.tracker}\nQuantidade de anos no banco de dados: {len(self.years)}")
        if len(self.years) == 1:
            self.single_year_label.configure(text=f"Ano: {self.bottom_year}")
            self.show_single_year_frame()
            self.main_frame.grid_rowconfigure(1, weight=6)
            self.main_frame.grid_rowconfigure(2, weight=0, uniform="")
        else:
            self.top_year_label.configure(text=f"Maior ano: {self.top_year}")
            self.bottom_year_label.configure(text=f"Menor ano: {self.bottom_year}")
            self.delete_top_year_btn.configure(command=partial(self.delete_year_popup, self.top_year))
            self.delete_bottom_year_btn.configure(command=partial(self.delete_year_popup, self.bottom_year))

    def delete_year_popup(self, year):
        if hasattr(self, "popup_frame"):
            self.popup_frame.destroy()

        self.popup_frame = DeleteYearView(
            self.winfo_toplevel(), 
            on_save=partial(self.remove_year, year), 
            year=year
        )

        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.popup_frame.wait_visibility()
        self.popup_frame.grab_set()

    def build_top_label(self):
        self.top_label_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="transparent")
        self.top_label_frame.grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        self.top_label_frame.grid_columnconfigure(0, weight=1)

        text = f"Marcador: {self.tracker}\nQuantidade de anos no banco de dados: {len(self.years)}"

        self.top_label = ctk.CTkLabel(self.top_label_frame, font=ctk.CTkFont(size=20, weight="bold"), text=text, corner_radius=10)
        self.top_label.grid(row=0, column=0, sticky="we")
    
    def build_top_year(self):
        self.top_year_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, height=60)
        
        self.top_year_frame.grid_columnconfigure(0, weight=1)
        self.top_year_frame.grid_rowconfigure(0, weight=1)

        self.top_year_label = ctk.CTkLabel(self.top_year_frame, font=ctk.CTkFont(size=20, weight="bold"), text=f"Maior ano: {self.top_year}", corner_radius=10)
        self.top_year_label.grid(row=0, column=0, padx=20, sticky="w")
        
        self.delete_top_year_btn = IconButton(
            parent=self.top_year_frame,
            command=partial(self.delete_year_popup, self.top_year),
            icon_type=IconType.BIG_TRASH,
            fg_color="transparent",
            height=60,
            width=60
        )
        self.delete_top_year_btn.grid(row=0, column=1, padx=20, pady=5, sticky="w")

    def build_bottom_year(self):
        self.bottom_year_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, height=60)
        
        self.bottom_year_frame.grid_columnconfigure(0, weight=1)
        self.bottom_year_frame.grid_rowconfigure(0, weight=1)
        
        self.bottom_year_label = ctk.CTkLabel(self.bottom_year_frame, font=ctk.CTkFont(size=20, weight="bold"), text=f"Menor ano: {self.bottom_year}", corner_radius=10)
        self.bottom_year_label.grid(row=0, column=0, padx=20, sticky="w")

        self.delete_bottom_year_btn = IconButton(
            parent=self.bottom_year_frame,
            command=partial(self.delete_year_popup, self.bottom_year),
            icon_type=IconType.BIG_TRASH,
            fg_color="transparent",
            height=60,
            width=60
        )
        self.delete_bottom_year_btn.grid(row=0, column=1, padx=20, pady=5, sticky="w")

    def build_single_year(self):
        self.single_year_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="transparent")
        self.single_year_frame.grid_columnconfigure(0, weight=1)
        self.single_year_frame.grid_rowconfigure((0, 1), weight=1)

        self.single_year_label_frame = ctk.CTkFrame(self.single_year_frame, corner_radius=10, fg_color="#333333")
        self.single_year_label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.single_year_label_frame.grid_columnconfigure(0, weight=1)
        self.single_year_label_frame.grid_rowconfigure(0, weight=1)
        
        self.single_year_label = ctk.CTkLabel(self.single_year_label_frame, font=ctk.CTkFont(size=20, weight="bold"), text=f"Ano: {self.bottom_year}", corner_radius=10)
        self.single_year_label.grid(row=0, column=0, pady=20, sticky="nsew")

        self.warning_label = ctk.CTkLabel(self.single_year_frame, font=ctk.CTkFont(size=20), text="Único ano salvo na memória.\n\nUm marcador deve\nconter pelo menos um ano.", text_color="grey")
        self.warning_label.grid(row=1, column=0, pady=20, sticky="nsew")

    def build_back_button(self):
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)

        self.back_button = CustomButton(self.button_frame, text="Voltar", command=self.destroy, font_size=15, height=35)
        self.back_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def show_double_year_frame(self):
        self.single_year_frame.grid_forget()
        self.bottom_year_frame.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")
        self.top_year_frame.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")
    
    def show_single_year_frame(self):
        self.top_year_frame.grid_forget()
        self.bottom_year_frame.grid_forget()
        self.single_year_frame.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=2, uniform="main")
        self.main_frame.grid_rowconfigure((1, 2), weight=3, uniform="main")

        self.build_top_label()
        self.build_top_year()
        self.build_bottom_year()
        self.build_single_year()

        if len(self.years) > 1:
            self.show_double_year_frame()
        else:
            self.show_single_year_frame()
            self.main_frame.grid_rowconfigure(1, weight=6)
            self.main_frame.grid_rowconfigure(2, weight=0, uniform="")

        self.build_back_button()
        