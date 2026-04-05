import pytest

from pages.dashboard_page import DashboardPage
from pages.add_employee_page import AddEmployeePage
from pages.employee_search_page import EmployeeSearchPage
from data.employee_data import EMPLOYEE_1


@pytest.fixture
def created_employee(admin_login):
    page = admin_login

    dashboard = DashboardPage(page)
    employee = AddEmployeePage(page)
    full_name = " ".join(
        (EMPLOYEE_1["first"], EMPLOYEE_1["middle"], EMPLOYEE_1["last"])
    )

    dashboard.go_to_pim()
    employee.add_employee(EMPLOYEE_1)
    return {
        "page": page,
        "employee_id": employee.get_employee_id(),
        "full_name": full_name,
    }


@pytest.mark.parametrize(
    "search_field",
    ["name", "id"],
    ids=["search-by-name", "search-by-id"],
)
def test_search_employee(created_employee, search_field):
    page = created_employee["page"]
    search = EmployeeSearchPage(page)
    search_value = (
        created_employee["full_name"]
        if search_field == "name"
        else created_employee["employee_id"]
    )

    search.open_pim()
    getattr(search, f"search_by_{search_field}")(search_value)
    search.open_result(created_employee["employee_id"], created_employee["full_name"])
