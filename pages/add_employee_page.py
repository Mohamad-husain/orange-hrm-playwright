import re
from playwright.sync_api import Page, expect
from utils.waits import wait_for_url_match


class AddEmployeePage:
    """Page object for Add Employee page."""

    def __init__(self, page: Page):
        self.page = page

    def _input_in_group(self, label_text: str):
        return self.page.locator(
            ".oxd-input-group",
            has=self.page.locator("label", has_text=label_text),
        ).locator("input").first

    @staticmethod
    def _profile_heading_name(employee_data):
        return " ".join(
            part for part in (employee_data["first"], employee_data["last"]) if part
        )

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
        return self._input_in_group("Username")

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
        return self._input_in_group("Employee Id")

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
        wait_for_url_match(self.page, r".*/pim/viewPersonalDetails/.*", timeout_ms=60000)
        self.expect_personal_details_page(employee_data)

    def expect_personal_details_page(self, employee_data):
        expected_heading = self._profile_heading_name(employee_data)
        expect(self.page).to_have_url(
            re.compile(r".*/pim/viewPersonalDetails/empNumber/\d+$")
        )
        expect(
            self.page.get_by_role("heading", name=expected_heading, exact=True)
        ).to_be_visible()
        expect(
            self.page.get_by_role("heading", name="Personal Details", exact=True)
        ).to_be_visible()

    def get_employee_id(self):
        """Return Employee ID from the page after saving."""
        self.page.wait_for_load_state("networkidle")
        expect(self.employee_id_input).to_have_value(re.compile(r"\S+"))
        return self.employee_id_input.input_value().strip()
