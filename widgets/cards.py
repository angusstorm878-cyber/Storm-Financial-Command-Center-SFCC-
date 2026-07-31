import customtkinter as ctk


class DashboardCard(ctk.CTkFrame):

    def __init__(self, parent, title, value):

        super().__init__(
            parent,
            corner_radius=12
        )

        self.configure(
            width=250,
            height=140
        )

        self.grid_propagate(False)


        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 16, "bold")
        )

        self.title_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20,10)
        )


        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=("Segoe UI", 28, "bold")
        )

        self.value_label.grid(
            row=1,
            column=0,
            padx=20
        )


    def update_value(self, value):

        self.value_label.configure(
            text=value
        )