import customtkinter as ctk

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        label = ctk.CTkLabel(
            self,
            text="Calendar",
            font=("Segoe UI", 30, "bold")
        )
        label.pack(expand=True)