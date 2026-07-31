import customtkinter as ctk

import config

from database import initialize_database
from widgets.sidebar import Sidebar

initialize_database()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title(config.APP_NAME)
app.geometry(f"{config.WIDTH}x{config.HEIGHT}")

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

sidebar = Sidebar(app)
sidebar.grid(row=0, column=0, sticky="ns")

content = ctk.CTkFrame(app)
content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

welcome = ctk.CTkLabel(
    content,
    text="Welcome to Storm Financial Command Center",
    font=("Segoe UI", 28, "bold")
)
welcome.pack(pady=50)

app.mainloop()