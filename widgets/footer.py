import customtkinter as ctk


class Footer(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, height=35)

        version = ctk.CTkLabel(
            self,
            text="SFCC Version 0.2"
        )

        version.pack(side="left", padx=20)

        author = ctk.CTkLabel(
            self,
            text="© 2026 Angus Storm"
        )

        author.pack(side="right", padx=20)