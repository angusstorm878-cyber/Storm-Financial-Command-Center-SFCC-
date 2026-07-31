import customtkinter as ctk

from widgets.cards import DashboardCard


class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.grid_columnconfigure((0, 1), weight=1)

        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Segoe UI", 32, "bold")
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Welcome back, Angus",
            font=("Segoe UI", 16)
        )

        subtitle.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 20)
        )

        cards = [
            ("Net Worth", "$0.00"),
            ("Investments", "$291.57"),
            ("Monthly Income", "$0.00"),
            ("Monthly Expenses", "$0.00"),
        ]

        row = 2
        column = 0

        for title, value in cards:

            card = DashboardCard(
                self,
                title,
                value
            )

            card.grid(
                row=row,
                column=column,
                padx=20,
                pady=20,
                sticky="nsew"
            )

            column += 1

            if column > 1:
                column = 0
                row += 1