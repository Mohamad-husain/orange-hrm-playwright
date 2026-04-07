import re
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect
from utils.waits import wait_for_url_match


class VacanciesPage:
    """Page object for vacancy creation inside Recruitment."""

    def __init__(self, page: Page):
        self.page = page

    def _group_by_label(self, label_text: str):
        return self.page.locator(
            ".oxd-input-group",
            has=self.page.locator("label", has_text=label_text),
        )

    def _input_in_group(self, label_text: str):
        return self._group_by_label(label_text).locator("input, textarea").first

    def _select_in_group(self, label_text: str):
        return self._group_by_label(label_text).locator(".oxd-select-text").first

    def _selected_text_in_group(self, label_text: str):
        return self._group_by_label(label_text).locator(".oxd-select-text-input").first

    @property
    def vacancies_link(self):
        return self.page.get_by_role("link", name="Vacancies")

    @property
    def add_button(self):
        return self.page.get_by_role("button", name="Add")

    @property
    def vacancy_name_input(self):
        return self._input_in_group("Vacancy Name")

    @property
    def job_title_dropdown(self):
        return self._select_in_group("Job Title")

    @property
    def selected_job_title(self):
        return self._selected_text_in_group("Job Title")

    @property
    def description_input(self):
        return self._input_in_group("Description")

    @property
    def hiring_manager_input(self):
        return self._input_in_group("Hiring Manager")

    @property
    def positions_input(self):
        return self._input_in_group("Number of Positions")

    @property
    def save_button(self):
        return self.page.get_by_role("button", name="Save")

    @property
    def active_switch(self):
        return self.page.locator(".oxd-switch-input").first

    @property
    def vacancy_filter_dropdown(self):
        return self.page.locator(".oxd-select-text").nth(1)

    @property
    def search_button(self):
        return self.page.get_by_role("button", name="Search")

    @property
    def confirm_delete_button(self):
        return self.page.get_by_role("button", name="Yes, Delete")

    def open_vacancies(self):
        expect(self.vacancies_link).to_be_visible()
        self.vacancies_link.click()
        self.page.wait_for_url("**/recruitment/viewJobVacancy")
        self.page.wait_for_load_state("networkidle")
        expect(self.add_button).to_be_visible()

    def add_vacancy(self, vacancy_data):
        self.add_button.click()
        self.vacancy_name_input.fill(vacancy_data["name"])
        self.job_title_dropdown.click()
        job_title_option = self.page.get_by_role(
            "option", name=vacancy_data["job_title"], exact=True
        )
        expect(job_title_option).to_be_visible()
        job_title_option.click()
        self.description_input.fill(vacancy_data["description"])
        self.hiring_manager_input.fill(vacancy_data["hiring_manager_hint"])
        hiring_manager_option = self.page.get_by_role(
            "option", name=vacancy_data["hiring_manager"], exact=True
        )
        expect(hiring_manager_option).to_be_visible()
        hiring_manager_option.click()
        self.positions_input.fill(vacancy_data["positions"])
        if self.active_switch.is_checked() != vacancy_data["active"]:
            self.active_switch.click()
        self.save_button.click()
        wait_for_url_match(
            self.page, r".*/recruitment/addJobVacancy/\d+$", timeout_ms=30000
        )
        self.expect_vacancy_details(vacancy_data)

    def expect_vacancy_details(self, vacancy_data):
        expect(self.page).to_have_url(re.compile(r".*/recruitment/addJobVacancy/\d+$"))
        expect(self.page.get_by_role("heading", name="Edit Vacancy")).to_be_visible()
        expect(self.vacancy_name_input).to_have_value(vacancy_data["name"])
        expect(self.selected_job_title).to_have_text(vacancy_data["job_title"])
        expect(self.hiring_manager_input).to_have_value(vacancy_data["hiring_manager"])
        expect(self.positions_input).to_have_value(vacancy_data["positions"])
        assert self.active_switch.is_checked() == vacancy_data["active"]

    def search_by_vacancy_name(self, vacancy_name, strict=True):
        self.vacancy_filter_dropdown.click()
        vacancy_option = self.page.get_by_role(
            "option", name=vacancy_name, exact=True
        )
        try:
            vacancy_option.wait_for(state="visible", timeout=3000)
        except PlaywrightTimeoutError:
            if strict:
                raise
            return False

        vacancy_option.click()
        self.search_button.click()
        self.page.wait_for_load_state("networkidle")
        return True

    def delete_vacancies_by_name(self, vacancy_name):
        deleted_count = 0
        while True:
            matching_rows = self.page.get_by_role("row").filter(has_text=vacancy_name)
            if matching_rows.count() == 0:
                return deleted_count

            matching_rows.first.locator("button").nth(0).click()
            expect(self.confirm_delete_button).to_be_visible()
            self.confirm_delete_button.click()
            self.page.wait_for_load_state("networkidle")
            deleted_count += 1
