from playwright.sync_api import Page, expect
from data.constants import BASE_URL, LOGIN_PATH


class LoginPage:
    """Page object for login page."""
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.dashboard_heading = page.get_by_role("heading", name="Dashboard")

    def navigate(self, base_url: str | None = None):
        app_base_url = base_url or BASE_URL
        self.page.goto(f"{app_base_url.rstrip('/')}{LOGIN_PATH}")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_url("**/dashboard/index")
        expect(self.dashboard_heading).to_be_visible()
