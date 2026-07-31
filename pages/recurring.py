import customtkinter as ctk

from database import (
    add_recurring_transaction,
    get_recurring_transactions,
    delete_recurring_transaction
)



class RecurringPage(ctk.CTkFrame):

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
            text="Recurring Transactions",
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



        self.type_menu = ctk.CTkOptionMenu(
            input_frame,
            values=[
                "Expense",
                "Income"
            ]
        )

        self.type_menu.set(
            "Expense"
        )

        self.type_menu.grid(
            row=0,
            column=3,
            padx=10,
            pady=10
        )



        self.frequency_menu = ctk.CTkOptionMenu(
            input_frame,
            values=[
                "Weekly",
                "Biweekly",
                "Monthly",
                "Yearly"
            ]
        )

        self.frequency_menu.set(
            "Monthly"
        )

        self.frequency_menu.grid(
            row=0,
            column=4,
            padx=10,
            pady=10
        )



        self.date_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="YYYY-MM-DD"
        )

        self.date_entry.grid(
            row=0,
            column=5,
            padx=10,
            pady=10
        )



        save_button = ctk.CTkButton(
            input_frame,
            text="Save",
            command=self.save_recurring
        )

        save_button.grid(
            row=0,
            column=6,
            padx=10,
            pady=10
        )



        # ==========================
        # DISPLAY SECTION
        # ==========================

        self.container = ctk.CTkScrollableFrame(
            self
        )

        self.container.grid(
            row=2,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )


        self.load_recurring()



    def save_recurring(self):

        description = self.description_entry.get()

        category = self.category_entry.get()


        try:

            amount = float(
                self.amount_entry.get()
            )

        except ValueError:

            return



        transaction_type = self.type_menu.get()

        frequency = self.frequency_menu.get()

        next_date = self.date_entry.get()



        add_recurring_transaction(
            description,
            category,
            amount,
            transaction_type,
            frequency,
            next_date
        )


        self.clear_inputs()

        self.load_recurring()



    def clear_inputs(self):

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

        self.date_entry.delete(
            0,
            "end"
        )



    def load_recurring(self):

        for widget in self.container.winfo_children():

            widget.destroy()



        recurring = get_recurring_transactions()


        if not recurring:

            label = ctk.CTkLabel(
                self.container,
                text="No recurring transactions."
            )

            label.pack(
                pady=20
            )

            return



        for item in recurring:

            self.create_card(item)



    def create_card(self, item):

        recurring_id = item[0]

        description = item[1]

        category = item[2]

        amount = item[3]

        transaction_type = item[4]

        frequency = item[5]

        next_date = item[6]



        card = ctk.CTkFrame(
            self.container,
            corner_radius=12
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )



        info = ctk.CTkLabel(
            card,
            text=(
                f"{description}\n\n"
                f"Category: {category}\n"
                f"Amount: ${amount:,.2f}\n"
                f"Type: {transaction_type}\n"
                f"Frequency: {frequency}\n"
                f"Next Date: {next_date}"
            ),
            justify="left"
        )

        info.pack(
            side="left",
            padx=20,
            pady=15
        )



        delete_button = ctk.CTkButton(
            card,
            text="Delete",
            width=80,
            command=lambda i=recurring_id: self.delete_recurring(i)
        )

        delete_button.pack(
            side="right",
            padx=20
        )



    def delete_recurring(self, recurring_id):

        delete_recurring_transaction(
            recurring_id
        )

        self.load_recurring()