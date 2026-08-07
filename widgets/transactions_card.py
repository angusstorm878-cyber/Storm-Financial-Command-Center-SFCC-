import customtkinter as ctk

from database import delete_transaction


class TransactionCard(ctk.CTkFrame):

    def __init__(
            self,
            parent,
            transaction,
            refresh_callback=None
    ):

        super().__init__(parent)

        self.transaction = transaction
        self.refresh_callback = refresh_callback

        transaction_id = transaction[0]
        date = transaction[1]
        category = transaction[2]
        description = transaction[3]
        amount = transaction[4]
        transaction_type = transaction[5]

        if transaction_type == "Income":
            symbol = "+"
        else:
            symbol = "-"

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_columnconfigure(
            1,
            weight=0
        )

        description_label = ctk.CTkLabel(
            self,
            text=description,
            font=("Segoe UI", 18, "bold")
        )

        description_label.grid(
            row=0,
            column=0,
            padx=15,
            pady=(12, 2),
            sticky="w"
        )

        amount_label = ctk.CTkLabel(
            self,
            text=f"{symbol}${amount:,.2f}",
            font=("Segoe UI", 18, "bold")
        )

        amount_label.grid(
            row=0,
            column=1,
            padx=15,
            pady=(12, 2),
            sticky="e"
        )

        details_label = ctk.CTkLabel(
            self,
            text=f"{category} | {date}",
            font=("Segoe UI", 13)
        )

        details_label.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 12),
            sticky="w"
        )

        delete_button = ctk.CTkButton(
            self,
            text="Delete",
            width=80,
            command=lambda:
                self.delete_transaction(
                    transaction_id
                )
        )

        delete_button.grid(
            row=1,
            column=1,
            padx=15,
            pady=(0, 12),
            sticky="e"
        )

    def delete_transaction(
            self,
            transaction_id
    ):

        delete_transaction(
            transaction_id
        )

        if self.refresh_callback:

            self.refresh_callback()