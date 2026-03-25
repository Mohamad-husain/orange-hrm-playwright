# tests/test_employee_search.py
from pages.dashboard_page import DashboardPage
from pages.add_employee_page import AddEmployeePage
from pages.employee_search_page import EmployeeSearchPage
from data.employee_data import EMPLOYEE_1

def test_search_employee(admin_login):
    page = admin_login

    dashboard = DashboardPage(page)
    employee = AddEmployeePage(page)
    search = EmployeeSearchPage(page)

    dashboard.go_to_pim()
    employee.add_employee(EMPLOYEE_1)
    emp_id = employee.get_employee_id()
    search.open_pim()
    search.search_by_name(f"{EMPLOYEE_1['first']} {EMPLOYEE_1['middle']} {EMPLOYEE_1['last']}")
    search.open_pim()
    search.search_by_id(emp_id)
    search.open_result(emp_id, f"{EMPLOYEE_1['first']} {EMPLOYEE_1['middle']} {EMPLOYEE_1['last']}")