from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.add_employee_page import AddEmployeePage
from data.employee_data import EMPLOYEE_1, EMPLOYEE_2

def test_add_employee_without_login(page: Page):

    login = LoginPage(page)
    dashboard = DashboardPage(page)
    employee = AddEmployeePage(page)

    login.navigate()
    login.login("Admin", "admin123")

    dashboard.go_to_pim()

    employee.add_employee(
        EMPLOYEE_1["first"],
        EMPLOYEE_1["middle"],
        EMPLOYEE_1["last"]
    )

    employee.save()


def test_add_employee_with_login(page: Page):

    login = LoginPage(page)
    dashboard = DashboardPage(page)
    employee = AddEmployeePage(page)

    login.navigate()
    login.login("Admin", "admin123")

    dashboard.go_to_pim()

    employee.add_employee(
        EMPLOYEE_2["first"],
        EMPLOYEE_2["middle"],
        EMPLOYEE_2["last"]
    )

    employee.add_login_details(
        EMPLOYEE_2["username"],
        EMPLOYEE_2["password"]
    )

    employee.save()