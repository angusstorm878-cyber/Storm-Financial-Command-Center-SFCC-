import customtkinter as ctk

from database import (
    add_receipt,
    get_receipts,
    delete_receipt
)


class ReceiptsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)


        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            2,
            weight=1
        )


        title = ctk.CTkLabel(
            self,
            text="Receipt Manager",
            font=("Segoe UI", 32, "bold")
        )

        title.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20,10),
            sticky="w"
        )


        # ==========================
        # INPUT SECTION
        # ==========================

        input_frame = ctk.CTkFrame(
            self
        )

        input_frame.grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky="ew"
        )


        self.vendor_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Vendor"
        )

        self.vendor_entry.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )


        self.amount_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Amount"
        )

        self.amount_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )


        self.notes_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Notes"
        )

        self.notes_entry.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )


        save_button = ctk.CTkButton(
            input_frame,
            text="Save Receipt",
            command=self.save_receipt
        )

        save_button.grid(
            row=0,
            column=3,
            padx=10,
            pady=10
        )


        # ==========================
        # RECEIPT DISPLAY
        # ==========================

        self.receipt_container = ctk.CTkScrollableFrame(
            self
        )

        self.receipt_container.grid(
            row=2,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )


        self.load_receipts()



    def save_receipt(self):

        vendor = self.vendor_entry.get()
        notes = self.notes_entry.get()


        if not vendor:
            return


        try:

            amount = float(
                self.amount_entry.get()
            )

        except ValueError:

            return



        add_receipt(
            vendor,
            amount,
            "",
            notes
        )


        self.vendor_entry.delete(
            0,
            "end"
        )


        self.amount_entry.delete(
            0,
            "end"
        )


        self.notes_entry.delete(
            0,
            "end"
        )


        self.load_receipts()



    def load_receipts(self):

        for widget in self.receipt_container.winfo_children():

            widget.destroy()


        receipts = get_receipts()


        if not receipts:

            label = ctk.CTkLabel(
                self.receipt_container,
                text="No receipts saved."
            )

            label.pack(
                pady=20
            )

            return



        for receipt in receipts:

            self.create_receipt_card(
                receipt
            )



    def create_receipt_card(
            self,
            receipt
    ):

        receipt_id = receipt[0]
        vendor = receipt[1]


        try:

            amount = float(
                receipt[2]
            )

        except (ValueError, TypeError):

            amount = 0


        notes = receipt[3]


        card = ctk.CTkFrame(
            self.receipt_container
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )


        info = ctk.CTkLabel(
            card,
            text=(
                f"{vendor}\n"
                f"${amount:,.2f}\n"
                f"{notes}"
            ),
            font=(
                "Segoe UI",
                15
            )
        )

        info.pack(
            side="left",
            padx=20,
            pady=10
        )


        delete_button = ctk.CTkButton(
            card,
            text="Delete",
            width=80,
            command=lambda i=receipt_id:
                self.delete_receipt(i)
        )

        delete_button.pack(
            side="right",
            padx=20
        )



    def delete_receipt(
            self,
            receipt_id
    ):

        delete_receipt(
            receipt_id
        )

        self.load_receipts()