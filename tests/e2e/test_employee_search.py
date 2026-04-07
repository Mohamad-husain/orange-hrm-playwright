import pytest

from pages.employee_search_page import EmployeeSearchPage
from data.employee_data import EMPLOYEE_1


@pytest.fixture
def created_employee(employee_factory):
    return employee_factory(EMPLOYEE_1)


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
