import re

# pylint: disable=duplicate-code

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect

from utils.waits import wait_for_url_match


class CandidatesPage:
    """Page object for candidate workflows inside Recruitment."""

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

    @property
    def add_button(self):
        return self.page.get_by_role("button", name="Add")

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
    def vacancy_dropdown(self):
        return self._select_in_group("Vacancy")

    @property
    def email_input(self):
        return self._input_in_group("Email")

    @property
    def candidate_name_input(self):
        return self._input_in_group("Candidate Name")

    @property
    def search_button(self):
        return self.page.get_by_role("button", name="Search")

    @property
    def save_button(self):
        return self.page.get_by_role("button", name="Save")

    @property
    def confirm_delete_button(self):
        return self.page.get_by_role("button", name="Yes, Delete")

    def open_candidates(self):
        expect(self.add_button).to_be_visible()
        expect(self.page).to_have_url(re.compile(r".*/recruitment/viewCandidates"))

    def add_candidate(self, candidate_data):
        self.add_button.click()
        expect(self.page.get_by_role("heading", name="Add Candidate")).to_be_visible()
        self.first_name_input.fill(candidate_data.first)
        self.middle_name_input.fill(candidate_data.middle)
        self.last_name_input.fill(candidate_data.last)
        self.vacancy_dropdown.click()
        vacancy_option = self.page.get_by_role(
            "option", name=candidate_data.vacancy_name, exact=True
        )
        expect(vacancy_option).to_be_visible()
        vacancy_option.click()
        self.email_input.fill(candidate_data.email)
        self.save_button.click()
        wait_for_url_match(
            self.page, r".*/recruitment/addCandidate/\d+$", timeout_ms=30000
        )
        self.expect_application_stage(candidate_data)

    def expect_application_stage(self, candidate_data):
        expect(self.page.get_by_role("heading", name="Application Stage")).to_be_visible()
        expect(self.page.get_by_text(candidate_data.full_name, exact=True)).to_be_visible()

    def change_application_stage(self, action, expected_status):
        self.page.get_by_role("button", name=action).click()
        expect(self.save_button).to_be_visible()
        self.save_button.click()
        self.page.wait_for_load_state("networkidle")
        expect(self.page.get_by_text(f"Status: {expected_status}")).to_be_visible()

    def search_by_candidate_name(self, full_name, strict=True):
        self.candidate_name_input.fill(full_name)
        candidate_option = self.page.get_by_role("option").filter(has_text=full_name).first
        option_timeout = 10000 if strict else 3000
        try:
            candidate_option.wait_for(state="visible", timeout=option_timeout)
        except PlaywrightTimeoutError:
            if strict:
                raise
            return False

        candidate_option.click()
        self.search_button.click()
        self.page.wait_for_load_state("networkidle")
        return True

    def delete_candidates_by_name(self, full_name):
        deleted_count = 0
        while deleted_count < 10:
            if not self.search_by_candidate_name(full_name, strict=False):
                return deleted_count

            matching_rows = self.page.get_by_role("row").filter(has_text=full_name)
            if matching_rows.count() == 0:
                return deleted_count

            matching_rows.first.locator("button").first.click()
            expect(self.confirm_delete_button).to_be_visible()
            self.confirm_delete_button.click()
            self.page.wait_for_load_state("networkidle")
            deleted_count += 1

        return deleted_count
