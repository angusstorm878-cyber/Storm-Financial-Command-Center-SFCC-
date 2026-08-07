import customtkinter as ctk

import os

from tkinter import filedialog

from database import (
    add_receipt,
    get_receipts,
    delete_receipt
)



class ReceiptsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)


        self.selected_file = ""


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



        attach_button = ctk.CTkButton(
            input_frame,
            text="Attach File",
            command=self.select_file
        )

        attach_button.grid(
            row=0,
            column=3,
            padx=10,
            pady=10
        )



        self.file_label = ctk.CTkLabel(
            input_frame,
            text="No file selected"
        )

        self.file_label.grid(
            row=1,
            column=0,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="w"
        )



        save_button = ctk.CTkButton(
            input_frame,
            text="Save Receipt",
            command=self.save_receipt
        )

        save_button.grid(
            row=0,
            column=4,
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



    # ==========================
    # FILE PICKER
    # ==========================

    def select_file(self):

        file = filedialog.askopenfilename(
            title="Select Receipt",
            filetypes=[
                (
                    "Receipt Files",
                    "*.png *.jpg *.jpeg *.pdf"
                )
            ]
        )


        if file:

            self.selected_file = file

            self.file_label.configure(
                text=os.path.basename(file)
            )



    # ==========================
    # SAVE RECEIPT
    # ==========================

    def save_receipt(self):

        vendor = self.vendor_entry.get()

        notes = self.notes_entry.get()


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
            self.selected_file,
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


        self.selected_file = ""


        self.file_label.configure(
            text="No file selected"
        )


        self.load_receipts()



    # ==========================
    # LOAD RECEIPTS
    # ==========================

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



    # ==========================
    # RECEIPT CARD
    # ==========================

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

        except:

            amount = 0



        category = receipt[3]

        file_path = receipt[4]

        notes = receipt[5]



        card = ctk.CTkFrame(
            self.receipt_container
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )



        attachment = "No Attachment"


        if file_path:

            attachment = (
                "📎 "
                +
                os.path.basename(file_path)
            )



        info = ctk.CTkLabel(
            card,
            text=(
                f"{vendor}\n"
                f"${amount:,.2f}\n"
                f"{notes}\n"
                f"{attachment}"
            ),
            font=(
                "Segoe UI",
                15
            ),
            justify="left"
        )


        info.pack(
            side="left",
            padx=20,
            pady=10
        )



        if file_path:

            open_button = ctk.CTkButton(
                card,
                text="Open",
                width=80,
                command=lambda p=file_path:
                    self.open_file(p)
            )


            open_button.pack(
                side="right",
                padx=5
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



    # ==========================
    # OPEN FILE
    # ==========================

    def open_file(
            self,
            path
    ):

        if os.path.exists(path):

            os.startfile(path)



    # ==========================
    # DELETE RECEIPT
    # ==========================

    def delete_receipt(
            self,
            receipt_id
    ):

        delete_receipt(
            receipt_id
        )


        self.load_receipts()