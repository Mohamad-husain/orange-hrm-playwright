from playwright.sync_api import Page, expect

class EmployeeSearchPage:
    """Page object for Employee List search."""
    def __init__(self, page: Page):
        self.page = page
        self.pim_menu = page.get_by_role("link", name="PIM")
        self.employee_name_input = page.get_by_role("textbox", name="Type for hints...").first
        self.search_button = page.get_by_role("button", name="Search")
        self.employee_id_input = page.get_by_role("textbox").nth(2)
        self.employee_name_option = page.get_by_role("option")

    def open_pim(self):
        self.pim_menu.click()
        self.page.wait_for_url("**/pim/viewEmployeeList")
        expect(self.search_button).to_be_visible()

    def _wait_for_results(self):
        self.page.wait_for_load_state("networkidle")
        expect(self.search_button).to_be_visible()

    def search_by_name(self, name):
        self.employee_name_input.fill(name)
        option = self.employee_name_option.filter(has_text=name).first
        expect(option).to_be_visible()
        option.click()
        self.search_button.click()
        self._wait_for_results()

    def search_by_id(self, emp_id):
        self.employee_id_input.fill(emp_id)
        self.search_button.click()
        self._wait_for_results()

    def open_result(self, emp_id, name):
        result_row = self.page.get_by_role("row", name=f"{emp_id} {name}")
        expect(result_row).to_be_visible()
        result_row.click()