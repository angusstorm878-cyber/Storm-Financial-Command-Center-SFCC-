import customtkinter as ctk


class Header(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, height=60)

        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Storm Financial Command Center",
            font=("Segoe UI", 22, "bold")
        )

        title.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        status = ctk.CTkLabel(
            self,
            text="🟢 ONLINE"
        )

        status.grid(row=0, column=1, padx=20)