import customtkinter as ctk

from widgets.cards import DashboardCard

from database import (
    get_monthly_summary,
    get_transactions,
    get_income_variance,
    get_upcoming_recurring_transactions
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
            7,
            weight=1
        )


        title = ctk.CTkLabel(
            self,
            text="Financial Command Center",
            font=("Segoe UI", 32, "bold")
        )


        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20,5)
        )



        subtitle = ctk.CTkLabel(
            self,
            text="Current financial position",
            font=("Segoe UI",16)
        )


        subtitle.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0,20)
        )



        self.create_cards()



        recurring_title = ctk.CTkLabel(
            self,
            text="Upcoming Recurring Transactions",
            font=("Segoe UI",20,"bold")
        )


        recurring_title.grid(
            row=5,
            column=0,
            sticky="w",
            padx=20,
            pady=(20,10)
        )



        self.recurring_box = ctk.CTkTextbox(
            self,
            height=150
        )


        self.recurring_box.grid(
            row=6,
            column=0,
            columnspan=2,
            padx=20,
            pady=10,
            sticky="nsew"
        )



        recent_title = ctk.CTkLabel(
            self,
            text="Recent Transactions",
            font=("Segoe UI",20,"bold")
        )


        recent_title.grid(
            row=7,
            column=0,
            sticky="w",
            padx=20,
            pady=(20,10)
        )



        self.transaction_box = ctk.CTkTextbox(
            self,
            height=200
        )


        self.transaction_box.grid(
            row=8,
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
            row=9,
            column=0,
            padx=20,
            pady=20,
            sticky="w"
        )


        self.load_dashboard()




    def create_cards(self):

        summary = get_monthly_summary()

        variance = get_income_variance()



        cards = [

            (
                "Monthly Income",
                f"${summary['income']:,.2f}"
            ),

            (
                "Monthly Expenses",
                f"${summary['expenses']:,.2f}"
            ),

            (
                "Cash Flow",
                f"${summary['net']:,.2f}"
            ),

            (
                "Income Variance",
                f"${variance:,.2f}"
            )

        ]



        row = 2
        column = 0



        for title,value in cards:


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





    def load_dashboard(self):

        self.load_recurring()

        self.load_transactions()




    def load_recurring(self):

        self.recurring_box.delete(
            "0.0",
            "end"
        )


        recurring = get_upcoming_recurring_transactions()



        if not recurring:

            self.recurring_box.insert(
                "end",
                "No upcoming recurring transactions.\n"
            )

            return



        for item in recurring[:5]:


            description = item[1]

            category = item[2]

            amount = item[3]

            transaction_type = item[4]

            next_date = item[6]



            symbol = "+"


            if transaction_type == "Expense":

                symbol = "-"



            self.recurring_box.insert(
                "end",
                f"{next_date} | {category} | {description} | {symbol}${amount:,.2f}\n"
            )





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

        summary = get_monthly_summary()

        variance = get_income_variance()



        self.cards["Monthly Income"].update_value(
            f"${summary['income']:,.2f}"
        )


        self.cards["Monthly Expenses"].update_value(
            f"${summary['expenses']:,.2f}"
        )


        self.cards["Cash Flow"].update_value(
            f"${summary['net']:,.2f}"
        )


        self.cards["Income Variance"].update_value(
            f"${variance:,.2f}"
        )



        self.load_dashboard()