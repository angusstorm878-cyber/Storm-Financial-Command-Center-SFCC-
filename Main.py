import customtkinter as ctk

import config

from database import initialize_database
from widgets.sidebar import Sidebar

from pages.dashboard import DashboardPage
from pages.calendar import CalendarPage
from pages.transactions import TransactionsPage
from pages.investments import InvestmentsPage
from pages.reports import ReportsPage
from pages.goals import GoalsPage
from pages.settings import SettingsPage
from pages.budgets import BudgetsPage
from pages.income import IncomePage


pages = {
    "Dashboard": DashboardPage,
    "Calendar": CalendarPage,
    "Transactions": TransactionsPage,
    "Investments": InvestmentsPage,
    "Reports": ReportsPage,
    "Goals": GoalsPage,
    "Settings": SettingsPage,
    "Budgets": BudgetsPage,
    "Income": IncomePage,
}


initialize_database()


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()


app.title(config.APP_NAME)

app.geometry(
    f"{config.WIDTH}x{config.HEIGHT}"
)


app.grid_columnconfigure(
    1,
    weight=1
)

app.grid_rowconfigure(
    0,
    weight=1
)



content = None



def show_page(page_name):

    global content


    if content:

        content.destroy()


    page_class = pages[page_name]


    content = page_class(app)


    content.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=20,
        pady=20
    )



sidebar = Sidebar(
    app,
    show_page
)


sidebar.grid(
    row=0,
    column=0,
    sticky="ns"
)



show_page(
    "Dashboard"
)



app.mainloop()