import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, width=220)

        buttons = [
            "Dashboard",
            "Calendar",
            "Transactions",
            "Investments",
            "Reports",
            "Goals",
            "Settings"
        ]

        for name in buttons:
            button = ctk.CTkButton(
                self,
                text=name,
                height=42
            )

            button.pack(fill="x", padx=15, pady=6)