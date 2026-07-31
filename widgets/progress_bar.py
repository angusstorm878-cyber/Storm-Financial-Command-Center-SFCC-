import customtkinter as ctk


class ProgressBar(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        percentage=0,
        width=300,
        height=20
    ):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.width = width
        self.height = height


        self.background = ctk.CTkFrame(
            self,
            width=self.width,
            height=self.height,
            corner_radius=10,
            fg_color=("gray70", "gray30")
        )

        self.background.pack()


        self.fill = ctk.CTkFrame(
            self.background,
            width=0,
            height=self.height,
            corner_radius=10,
            fg_color=("green", "green")
        )


        self.update_progress(
            percentage
        )



    def update_progress(
        self,
        percentage
    ):

        if percentage < 0:
            percentage = 0

        if percentage > 100:
            percentage = 100


        fill_width = int(
            self.width * (percentage / 100)
        )


        self.fill.configure(
            width=fill_width
        )


        self.fill.place(
            x=0,
            y=0
        )


        if percentage >= 100:

            self.fill.configure(
                fg_color=("red", "red")
            )

        elif percentage >= 75:

            self.fill.configure(
                fg_color=("orange", "orange")
            )

        else:

            self.fill.configure(
                fg_color=("green", "green")
            )