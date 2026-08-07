import customtkinter as ctk
from datetime import datetime

from widgets.transactions_card import TransactionCard

from database import (
    add_transaction,
    get_transactions,
    get_vendor_memory
)


class TransactionsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.build_title()
        self.build_input_area()
        self.build_transaction_list()

        self.load_transactions()


    # ==========================
    # TITLE
    # ==========================

    def build_title(self):

        title = ctk.CTkLabel(
            self,
            text="Transactions",
            font=("Segoe UI", 32, "bold")
        )

        title.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 10),
            sticky="w"
        )


    # ==========================
    # INPUT AREA
    # ==========================

    def build_input_area(self):

        input_frame = ctk.CTkFrame(self)

        input_frame.grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky="ew"
        )

        self.description_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Description"
        )

        self.description_entry.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.description_entry.bind(
            "<FocusOut>",
            self.check_vendor_memory
        )

        self.category_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Category"
        )

        self.category_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        self.amount_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Amount"
        )

        self.amount_entry.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )

        self.type_entry = ctk.CTkComboBox(
            input_frame,
            values=[
                "Expense",
                "Income"
            ]
        )

        self.type_entry.grid(
            row=0,
            column=3,
            padx=10,
            pady=10
        )

        self.type_entry.set("Expense")

        self.date_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="YYYY-MM-DD"
        )

        self.date_entry.grid(
            row=0,
            column=4,
            padx=10,
            pady=10
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        add_button = ctk.CTkButton(
            input_frame,
            text="Add Transaction",
            command=self.save_transaction
        )

        add_button.grid(
            row=0,
            column=5,
            padx=10,
            pady=10
        )


    # ==========================
    # TRANSACTION LIST
    # ==========================

    def build_transaction_list(self):

        self.transaction_container = ctk.CTkScrollableFrame(
            self
        )

        self.transaction_container.grid(
            row=2,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )


    # ==========================
    # VENDOR MEMORY
    # ==========================

    def check_vendor_memory(
            self,
            event=None
    ):

        vendor = self.description_entry.get().strip()

        if not vendor:
            return

        vendor_memory = get_vendor_memory(vendor)

        if not vendor_memory:
            return

        category = vendor_memory[2]

        self.category_entry.delete(
            0,
            "end"
        )

        self.category_entry.insert(
            0,
            category
        )


    # ==========================
    # SAVE TRANSACTION
    # ==========================

    def save_transaction(self):

        description = self.description_entry.get().strip()
        category = self.category_entry.get().strip()
        transaction_type = self.type_entry.get()
        transaction_date = self.date_entry.get().strip()

        if not description:
            return

        if not category:
            return

        try:
            amount = float(
                self.amount_entry.get()
            )

        except ValueError:
            return

        add_transaction(
            description,
            category,
            amount,
            transaction_type,
            transaction_date
        )

        self.clear_form()
        self.load_transactions()


    # ==========================
    # CLEAR FORM
    # ==========================

    def clear_form(self):

        self.description_entry.delete(
            0,
            "end"
        )

        self.category_entry.delete(
            0,
            "end"
        )

        self.amount_entry.delete(
            0,
            "end"
        )

        self.type_entry.set("Expense")

        self.date_entry.delete(
            0,
            "end"
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )


    # ==========================
    # LOAD TRANSACTIONS
    # ==========================

    def load_transactions(self):

        for widget in self.transaction_container.winfo_children():
            widget.destroy()

        transactions = get_transactions()

        if not transactions:

            empty_label = ctk.CTkLabel(
                self.transaction_container,
                text="No transactions found."
            )

            empty_label.pack(
                pady=20
            )

            return

        for transaction in transactions:

            card = TransactionCard(
                self.transaction_container,
                transaction,
                refresh_callback=self.load_transactions
            )

            card.pack(
                fill="x",
                padx=10,
                pady=6
            )