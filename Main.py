import customtkinter as ctk

from database import initialize_database

import config

initialize_database()

ctk.set_appearance_mode("Dark")

ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title(config.APP_NAME)

app.geometry(f"{config.WIDTH}x{config.HEIGHT}")

app.mainloop()
