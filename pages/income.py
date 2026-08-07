import customtkinter as ctk

from database import (
    add_income_forecast,
    get_income_forecasts,
    get_income_variance,
    get_monthly_summary
)



class IncomePage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)


        self.grid_columnconfigure(
            0,
            weight=1
        )


        self.grid_rowconfigure(
            3,
            weight=1
        )



        # ==========================
        # TITLE
        # ==========================

        title = ctk.CTkLabel(
            self,
            text="Income Forecast",
            font=(
                "Segoe UI",
                32,
                "bold"
            )
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



        self.source_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Income Source"
        )


        self.source_entry.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )



        self.amount_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Expected Amount"
        )


        self.amount_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )



        save_button = ctk.CTkButton(
            input_frame,
            text="Save Forecast",
            command=self.save_forecast
        )


        save_button.grid(
            row=0,
            column=2,
            padx=10,
            pady=10
        )



        refresh_button = ctk.CTkButton(
            input_frame,
            text="Refresh",
            command=self.load_income
        )


        refresh_button.grid(
            row=0,
            column=3,
            padx=10,
            pady=10
        )



        # ==========================
        # SUMMARY
        # ==========================

        self.summary = ctk.CTkLabel(
            self,
            text="",
            font=(
                "Segoe UI",
                18
            ),
            justify="left"
        )


        self.summary.grid(
            row=2,
            column=0,
            padx=20,
            pady=10,
            sticky="w"
        )



        # ==========================
        # FORECAST LIST
        # ==========================

        self.forecast_container = ctk.CTkScrollableFrame(
            self
        )


        self.forecast_container.grid(
            row=3,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )



        self.load_income()



    # ==========================
    # SAVE FORECAST
    # ==========================

    def save_forecast(self):

        source = self.source_entry.get()


        try:

            amount = float(
                self.amount_entry.get()
            )

        except ValueError:

            return



        add_income_forecast(
            source,
            amount
        )


        self.source_entry.delete(
            0,
            "end"
        )


        self.amount_entry.delete(
            0,
            "end"
        )


        self.load_income()



    # ==========================
    # LOAD PAGE
    # ==========================

    def load_income(self):


        for widget in self.forecast_container.winfo_children():

            widget.destroy()



        forecasts = get_income_forecasts()



        expected = sum(
            item[2]
            for item in forecasts
        )


        summary = get_monthly_summary()

        actual = summary["income"]


        variance = get_income_variance()



        self.summary.configure(
            text=(
                f"Expected Income: ${expected:,.2f}\n"
                f"Actual Income: ${actual:,.2f}\n"
                f"Variance: ${variance:,.2f}"
            )
        )



        if not forecasts:

            empty = ctk.CTkLabel(
                self.forecast_container,
                text="No income forecasts created."
            )


            empty.pack(
                pady=20
            )


            return



        for income in forecasts:

            self.create_income_card(
                income
            )



    # ==========================
    # INCOME CARD
    # ==========================

    def create_income_card(
            self,
            income
    ):


        income_id = income[0]

        source = income[1]

        amount = income[2]


        card = ctk.CTkFrame(
            self.forecast_container,
            corner_radius=12
        )


        card.pack(
            fill="x",
            padx=10,
            pady=10
        )



        label = ctk.CTkLabel(
            card,
            text=(
                f"{source}\n"
                f"Expected: ${amount:,.2f}"
            ),
            font=(
                "Segoe UI",
                18,
                "bold"
            ),
            justify="left"
        )


        label.pack(
            side="left",
            padx=20,
            pady=15
        )



        delete_button = ctk.CTkButton(
            card,
            text="Delete",
            width=80,
            command=lambda i=income_id: self.delete_income(i)
        )


        delete_button.pack(
            side="right",
            padx=20
        )



    def delete_income(
            self,
            income_id
    ):

        delete_income_forecast(
            income_id
        )


        self.load_income()