import re
from playwright.sync_api import Page, expect


class AddEmployeePage:
    """Page object for Add Employee page."""

    def __init__(self, page: Page):
        self.page = page

    @property
    def add_employee_link(self):
        return self.page.get_by_role("link", name="Add Employee")

    @property
    def first_name_input(self):
        return self.page.get_by_role("textbox", name="First Name")

    @property
    def middle_name_input(self):
        return self.page.get_by_role("textbox", name="Middle Name")

    @property
    def last_name_input(self):
        return self.page.get_by_role("textbox", name="Last Name")

    @property
    def login_checkbox(self):
        return self.page.locator(".oxd-switch-input")

    @property
    def username_input(self):
        return self.page.get_by_role("textbox").nth(5)

    @property
    def password_input(self):
        return self.page.locator("input[type='password']").first

    @property
    def confirm_password_input(self):
        return self.page.locator("input[type='password']").nth(1)

    @property
    def save_button(self):
        return self.page.get_by_role("button", name="Save")

    @property
    def employee_id_input(self):
        return self.page.get_by_role("textbox").nth(4)

    def add_employee(self, employee_data, with_login=False):
        self.add_employee_link.click()
        self.first_name_input.fill(employee_data["first"])
        self.middle_name_input.fill(employee_data["middle"])
        self.last_name_input.fill(employee_data["last"])

        if with_login:
            self.login_checkbox.click()
            self.username_input.fill(employee_data["username"])
            self.password_input.fill(employee_data["password"])
            self.confirm_password_input.fill(employee_data["password"])

        self.save_button.click()
        self.page.wait_for_url("**/pim/viewPersonalDetails/**")

    def get_employee_id(self):
        """Return Employee ID from the page after saving."""
        self.page.wait_for_load_state("networkidle")
        expect(self.employee_id_input).to_have_value(re.compile(r"\S+"))
        return self.employee_id_input.input_value().strip()
