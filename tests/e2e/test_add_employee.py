from pages.dashboard_page import DashboardPage
from pages.add_employee_page import AddEmployeePage
from data.employee_data import EMPLOYEE_1, EMPLOYEE_2


def test_add_employee_without_login(admin_login):
    page = admin_login
    dashboard = DashboardPage(page)
    employee = AddEmployeePage(page)
    dashboard.go_to_pim()
    employee.add_employee(EMPLOYEE_1)


def test_add_employee_with_login(admin_login):
    page = admin_login
    dashboard = DashboardPage(page)
    employee = AddEmployeePage(page)
    dashboard.go_to_pim()
    employee.add_employee(EMPLOYEE_2, with_login=True)

