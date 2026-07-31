import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent, callback):

        super().__init__(
            parent,
            width=220,
            corner_radius=0
        )


        self.grid_rowconfigure(
            13,
            weight=1
        )



        title = ctk.CTkLabel(
            self,
            text="Storm\nFinancial\nCommand Center",
            font=("Segoe UI", 20, "bold")
        )


        title.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20,30)
        )



        buttons = [
            "Dashboard",
            "Calendar",
            "Budgets",
            "Transactions",
            "Receipts",
            "Recurring",
            "Investments",
            "Income",
            "Reports",
            "Goals",
            "Settings",
            
        ]



        for index, page in enumerate(buttons, start=1):

            button = ctk.CTkButton(
                self,
                text=page,
                width=180,
                command=lambda p=page: callback(p)
            )


            button.grid(
                row=index,
                column=0,
                padx=20,
                pady=5
            )



        status = ctk.CTkLabel(
            self,
            text="● System Online",
            text_color="lightgreen"
        )


        status.grid(
            row=12,
            column=0,
            pady=20
        )