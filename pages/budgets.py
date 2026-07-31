import customtkinter as ctk

from database import (
    add_budget,
    get_budgets,
    get_category_spending,
    update_budget,
    delete_budget
)

from widgets.progress_bar import ProgressBar



class BudgetsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)


        self.editing_budget_id = None


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
            text="Budget Tracking",
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


        self.category_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Category"
        )

        self.category_entry.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )


        self.amount_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Budget Amount"
        )

        self.amount_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )


        save_button = ctk.CTkButton(
            input_frame,
            text="Save Budget",
            command=self.save_budget
        )

        save_button.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )



        # ==========================
        # BUDGET DISPLAY
        # ==========================

        self.budget_container = ctk.CTkScrollableFrame(
            self
        )

        self.budget_container.grid(
            row=2,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )


        self.load_budgets()



    def save_budget(self):

        category = self.category_entry.get()


        try:

            amount = float(
                self.amount_entry.get()
            )

        except ValueError:

            return



        if self.editing_budget_id:


            update_budget(
                self.editing_budget_id,
                category,
                amount
            )


            self.editing_budget_id = None


        else:


            add_budget(
                category,
                amount
            )



        self.category_entry.delete(
            0,
            "end"
        )


        self.amount_entry.delete(
            0,
            "end"
        )


        self.load_budgets()



    def load_budgets(self):


        for widget in self.budget_container.winfo_children():

            widget.destroy()



        budgets = get_budgets()



        if not budgets:

            empty = ctk.CTkLabel(
                self.budget_container,
                text="No budgets created."
            )

            empty.pack(
                pady=20
            )

            return



        for budget in budgets:


            budget_id = budget[0]

            category = budget[1]

            limit = budget[2]



            spent = get_category_spending(
                category
            )



            if limit > 0:

                percentage = (
                    spent / limit
                ) * 100

            else:

                percentage = 0



            remaining = limit - spent



            if percentage >= 100:

                status = "OVER BUDGET"

            elif percentage >= 75:

                status = "WARNING"

            else:

                status = "HEALTHY"



            self.create_budget_card(
                budget_id,
                category,
                limit,
                spent,
                remaining,
                percentage,
                status
            )



    def create_budget_card(
            self,
            budget_id,
            category,
            limit,
            spent,
            remaining,
            percentage,
            status
    ):


        card = ctk.CTkFrame(
            self.budget_container,
            corner_radius=12
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )



        title = ctk.CTkLabel(
            card,
            text=category,
            font=("Segoe UI", 20, "bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(15,5)
        )



        numbers = ctk.CTkLabel(
            card,
            text=(
                f"${spent:,.2f} / "
                f"${limit:,.2f}"
            ),
            font=("Segoe UI",16)
        )

        numbers.pack(
            anchor="w",
            padx=20
        )



        bar = ProgressBar(
            card,
            percentage
        )

        bar.pack(
            padx=20,
            pady=10,
            fill="x"
        )



        remaining_label = ctk.CTkLabel(
            card,
            text=f"Remaining: ${remaining:,.2f}"
        )

        remaining_label.pack(
            anchor="w",
            padx=20
        )



        status_label = ctk.CTkLabel(
            card,
            text=f"Status: {status}",
            font=("Segoe UI",14,"bold")
        )

        status_label.pack(
            anchor="w",
            padx=20,
            pady=(5,10)
        )



        button_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=(0,15)
        )



        edit_button = ctk.CTkButton(
            button_frame,
            text="Edit",
            width=100,
            command=lambda: self.edit_budget(
                budget_id,
                category,
                limit
            )
        )

        edit_button.grid(
            row=0,
            column=0,
            padx=10
        )



        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete",
            width=100,
            fg_color="red",
            command=lambda: self.remove_budget(
                budget_id
            )
        )

        delete_button.grid(
            row=0,
            column=1,
            padx=10
        )



    def edit_budget(
            self,
            budget_id,
            category,
            amount
    ):


        self.editing_budget_id = budget_id


        self.category_entry.delete(
            0,
            "end"
        )

        self.amount_entry.delete(
            0,
            "end"
        )


        self.category_entry.insert(
            0,
            category
        )


        self.amount_entry.insert(
            0,
            str(amount)
        )



    def remove_budget(
            self,
            budget_id
    ):

        delete_budget(
            budget_id
        )

        self.load_budgets()