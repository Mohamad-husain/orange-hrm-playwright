import pytest
from pages.login_page import LoginPage
from data.constants import ADMIN_USERNAME, ADMIN_PASSWORD


@pytest.fixture
def admin_login(page):
    """Return a logged-in page using pytest-playwright's built-in page fixture."""
    login = LoginPage(page)
    login.navigate()
    login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
    page.wait_for_load_state("networkidle")
    return page
