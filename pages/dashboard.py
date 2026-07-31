import customtkinter as ctk

from widgets.cards import DashboardCard

from database import (
    get_monthly_income,
    get_monthly_expenses,
    get_net_worth,
    get_transactions
)


class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.cards = {}

        self.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        self.grid_rowconfigure(
            6,
            weight=1
        )


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


        self.create_cards()


        recent_title = ctk.CTkLabel(
            self,
            text="Recent Transactions",
            font=("Segoe UI", 20, "bold")
        )

        recent_title.grid(
            row=5,
            column=0,
            sticky="w",
            padx=20,
            pady=(30, 10)
        )


        self.transaction_box = ctk.CTkTextbox(
            self,
            height=200
        )

        self.transaction_box.grid(
            row=6,
            column=0,
            columnspan=2,
            padx=20,
            pady=10,
            sticky="nsew"
        )


        refresh_button = ctk.CTkButton(
            self,
            text="Refresh Dashboard",
            command=self.refresh_dashboard
        )

        refresh_button.grid(
            row=7,
            column=0,
            padx=20,
            pady=20,
            sticky="w"
        )


        self.load_transactions()


    def create_cards(self):

        income = get_monthly_income()
        expenses = get_monthly_expenses()
        net_worth = get_net_worth()


        cards = [
            ("Net Worth", f"${net_worth:,.2f}"),
            ("Investments", "$291.57"),
            ("Monthly Income", f"${income:,.2f}"),
            ("Monthly Expenses", f"${expenses:,.2f}")
        ]


        row = 2
        column = 0


        for title, value in cards:

            card = DashboardCard(
                self,
                title,
                value
            )

            self.cards[title] = card

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


    def load_transactions(self):

        self.transaction_box.delete(
            "0.0",
            "end"
        )


        transactions = get_transactions()


        for transaction in transactions[:5]:

            date = transaction[1]
            category = transaction[2]
            description = transaction[3]
            amount = transaction[4]
            transaction_type = transaction[5]


            symbol = "+"

            if transaction_type == "Expense":
                symbol = "-"


            self.transaction_box.insert(
                "end",
                f"{date} | {category} | {description} | {symbol}${amount:,.2f}\n"
            )


    def refresh_dashboard(self):

        income = get_monthly_income()
        expenses = get_monthly_expenses()
        net_worth = get_net_worth()


        self.cards["Net Worth"].update_value(
            f"${net_worth:,.2f}"
        )


        self.cards["Monthly Income"].update_value(
            f"${income:,.2f}"
        )


        self.cards["Monthly Expenses"].update_value(
            f"${expenses:,.2f}"
        )


        self.load_transactions()