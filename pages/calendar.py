import customtkinter as ctk


class CalendarPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        label = ctk.CTkLabel(
            self,
            text="Calendar",
            font=("Segoe UI", 30, "bold")
        )

        label.pack(pady=40)