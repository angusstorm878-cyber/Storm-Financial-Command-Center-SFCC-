import customtkinter as ctk

from database import (
    add_income_forecast,
    get_income_forecasts,
    get_actual_income,
    get_income_variance
)



class IncomePage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)


        self.grid_columnconfigure(
            0,
            weight=1
        )


        title = ctk.CTkLabel(
            self,
            text="Income Forecast",
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



        # ==========================
        # SUMMARY SECTION
        # ==========================

        self.summary = ctk.CTkTextbox(
            self,
            height=250
        )

        self.summary.grid(
            row=2,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )


        self.grid_rowconfigure(
            2,
            weight=1
        )


        self.load_income()



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



    def load_income(self):

        self.summary.delete(
            "1.0",
            "end"
        )


        forecasts = get_income_forecasts()


        expected = sum(
            item[2]
            for item in forecasts
        )


        actual = get_actual_income()


        variance = get_income_variance()



        self.summary.insert(
            "end",
            (
                f"INCOME FORECAST\n"
                f"=====================\n\n"

                f"Expected Income:\n"
                f"${expected:,.2f}\n\n"

                f"Actual Income:\n"
                f"${actual:,.2f}\n\n"

                f"Variance:\n"
                f"${variance:,.2f}\n\n"

                f"=====================\n"
            )
        )