import customtkinter as ctk

from widgets.sidebar import Sidebar
from widgets.header import Header
from widgets.footer import Footer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SFCC(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Storm Financial Command Center")
        self.geometry("1400x800")
        self.minsize(1200, 700)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.header = Header(self)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=1, column=0, sticky="ns")

        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.footer = Footer(self)
        self.footer.grid(row=2, column=0, columnspan=2, sticky="ew")


if __name__ == "__main__":
    app = SFCC()
    app.mainloop()
