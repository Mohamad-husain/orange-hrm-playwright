import re
from playwright.sync_api import Page, expect

class AddEmployeePage:
    """Page object for Add Employee page."""

    def __init__(self, page: Page):
        self.page = page
        self.add_employee_link = page.get_by_role("link", name="Add Employee")
        self.first_name = page.get_by_role("textbox", name="First Name")
        self.middle_name = page.get_by_role("textbox", name="Middle Name")
        self.last_name = page.get_by_role("textbox", name="Last Name")
        self.login_checkbox = page.locator(".oxd-switch-input")
        self.username = page.get_by_role("textbox").nth(5)
        self.password = page.locator("input[type='password']").first
        self.confirm_password = page.locator("input[type='password']").nth(1)
        self.save_button = page.get_by_role("button", name="Save")
        self.employee_id_input = page.get_by_role("textbox").nth(4)

    def add_employee(self, employee_data, with_login=False):
        self.add_employee_link.click()
        self.first_name.fill(employee_data["first"])
        self.middle_name.fill(employee_data["middle"])
        self.last_name.fill(employee_data["last"])

        if with_login:
            self.login_checkbox.click()
            self.username.fill(employee_data["username"])
            self.password.fill(employee_data["password"])
            self.confirm_password.fill(employee_data["password"])

        self.save_button.click()
        self.page.wait_for_url("**/pim/viewPersonalDetails/**")

    def get_employee_id(self):
        """Return Employee ID from the page after saving."""
        self.page.wait_for_load_state("networkidle")
        expect(self.employee_id_input).to_have_value(re.compile(r"\S+"))
        return self.employee_id_input.input_value().strip()
