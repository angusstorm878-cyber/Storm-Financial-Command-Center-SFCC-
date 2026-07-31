import customtkinter as ctk

from database import (
    add_transaction,
    get_transactions,
    delete_transaction
)


class TransactionsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)


        title = ctk.CTkLabel(
            self,
            text="Transactions",
            font=("Segoe UI", 30, "bold")
        )

        title.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20,10),
            sticky="w"
        )


        entry_frame = ctk.CTkFrame(self)

        entry_frame.grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky="ew"
        )


        self.description_entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Description"
        )

        self.description_entry.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )


        self.category_entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Category"
        )

        self.category_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )


        self.amount_entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Amount"
        )

        self.amount_entry.grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )


        self.type_menu = ctk.CTkOptionMenu(
            entry_frame,
            values=[
                "Income",
                "Expense"
            ]
        )

        self.type_menu.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )


        add_button = ctk.CTkButton(
            entry_frame,
            text="Add",
            command=self.add_transaction
        )

        add_button.grid(
            row=0,
            column=4,
            padx=5,
            pady=5
        )


        self.transaction_box = ctk.CTkTextbox(
            self,
            height=300
        )

        self.transaction_box.grid(
            row=2,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )


        delete_frame = ctk.CTkFrame(self)

        delete_frame.grid(
            row=3,
            column=0,
            padx=20,
            pady=10
        )


        self.delete_entry = ctk.CTkEntry(
            delete_frame,
            placeholder_text="Transaction ID"
        )

        self.delete_entry.grid(
            row=0,
            column=0,
            padx=5
        )


        delete_button = ctk.CTkButton(
            delete_frame,
            text="Delete",
            command=self.delete_transaction
        )

        delete_button.grid(
            row=0,
            column=1,
            padx=5
        )


        refresh_button = ctk.CTkButton(
            delete_frame,
            text="Refresh",
            command=self.load_transactions
        )

        refresh_button.grid(
            row=0,
            column=2,
            padx=5
        )


        self.load_transactions()


    def add_transaction(self):

        description = self.description_entry.get()
        category = self.category_entry.get()

        try:
            amount = float(
                self.amount_entry.get()
            )

        except ValueError:
            return


        transaction_type = self.type_menu.get()


        add_transaction(
            description,
            category,
            amount,
            transaction_type
        )


        self.load_transactions()


    def delete_transaction(self):

        try:
            transaction_id = int(
                self.delete_entry.get()
            )

        except ValueError:
            return


        delete_transaction(
            transaction_id
        )


        self.load_transactions()


    def load_transactions(self):

        self.transaction_box.delete(
            "0.0",
            "end"
        )


        transactions = get_transactions()


        for transaction in transactions:

            transaction_id = transaction[0]
            date = transaction[1]
            category = transaction[2]
            description = transaction[3]
            amount = transaction[4]
            transaction_type = transaction[5]


            sign = "+"

            if transaction_type == "Expense":
                sign = "-"


            line = (
                f"{transaction_id} | "
                f"{date} | "
                f"{category} | "
                f"{description} | "
                f"{sign}${amount:,.2f}\n"
            )


            self.transaction_box.insert(
                "end",
                line
            )