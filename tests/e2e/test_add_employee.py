from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.add_employee_page import AddEmployeePage
from data.employee_data import EMPLOYEE_1, EMPLOYEE_2
from data.constants import ADMIN_USERNAME, ADMIN_PASSWORD

def test_add_employee_without_login(page: Page):
    login = LoginPage(page)
    dashboard = DashboardPage(page)
    employee = AddEmployeePage(page)

    login.navigate()
    login.login(ADMIN_USERNAME, ADMIN_PASSWORD)

    dashboard.go_to_pim()
    employee.add_employee(EMPLOYEE_1)


def test_add_employee_with_login(page: Page):
    login = LoginPage(page)
    dashboard = DashboardPage(page)
    employee = AddEmployeePage(page)

    login.navigate()
    login.login(ADMIN_USERNAME, ADMIN_PASSWORD)

    dashboard.go_to_pim()
    employee.add_employee(EMPLOYEE_2, with_login=True)