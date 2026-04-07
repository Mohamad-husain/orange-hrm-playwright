from data.employee_data import EMPLOYEE_1, EMPLOYEE_2
from pages.add_employee_page import AddEmployeePage


def test_add_employee_without_login(employee_factory):
    created_employee = employee_factory(EMPLOYEE_1)
    AddEmployeePage(created_employee["page"]).expect_personal_details_page(EMPLOYEE_1)


def test_add_employee_with_login(employee_factory):
    created_employee = employee_factory(EMPLOYEE_2, with_login=True)
    AddEmployeePage(created_employee["page"]).expect_personal_details_page(EMPLOYEE_2)

