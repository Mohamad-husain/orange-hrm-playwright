from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect


class EmployeeSearchPage:
    """Page object for Employee List search."""

    def __init__(self, page: Page):
        self.page = page
        self.pim_menu = page.get_by_role("link", name="PIM")
        self.employee_name_input = (
            page.get_by_role("textbox", name="Type for hints...").first
        )
        self.search_button = page.get_by_role("button", name="Search")
        self.employee_id_input = page.get_by_role("textbox").nth(2)
        self.employee_name_option = page.get_by_role("option")
        self.confirm_delete_button = page.get_by_role("button", name="Yes, Delete")

    def open_pim(self):
        self.pim_menu.click()
        self.page.wait_for_url("**/pim/viewEmployeeList")
        expect(self.search_button).to_be_visible()

    def _wait_for_results(self):
        self.page.wait_for_load_state("networkidle")
        expect(self.search_button).to_be_visible()

    def search_by_name(self, name, strict=True):
        self.employee_name_input.fill(name)
        option = self.employee_name_option.filter(has_text=name).first
        option_timeout = 10000 if strict else 3000
        try:
            option.wait_for(state="visible", timeout=option_timeout)
        except PlaywrightTimeoutError:
            if strict:
                raise
            return False
        option.click()
        self.search_button.click()
        self._wait_for_results()
        return True

    def search_by_id(self, emp_id):
        self.employee_id_input.fill(emp_id)
        self.search_button.click()
        self._wait_for_results()

    def open_result(self, emp_id, name):
        result_row = self.page.get_by_role("row", name=f"{emp_id} {name}")
        expect(result_row).to_be_visible()
        result_row.click()

    def _delete_first_result_row(self):
        result_row = self.page.get_by_role("row").nth(1)
        result_row.locator("button").nth(1).click()
        expect(self.confirm_delete_button).to_be_visible()
        self.confirm_delete_button.click()
        self.page.wait_for_load_state("networkidle")

    def delete_employee_by_id(self, emp_id):
        self.open_pim()
        self.search_by_id(emp_id)
        if self.page.get_by_role("row").count() < 2:
            return False

        self._delete_first_result_row()
        return True

    def delete_employees_by_name(self, name):
        deleted_count = 0
        while deleted_count < 10:
            self.open_pim()
            if not self.search_by_name(name, strict=False):
                return deleted_count
            if self.page.get_by_role("row").count() < 2:
                return deleted_count

            self._delete_first_result_row()
            deleted_count += 1

        return deleted_count
