import pytest

from data.candidate_data import build_candidate_data
from data.vacancy_data import VACANCY_CASES, build_vacancy_data
from pages.candidates_page import CandidatesPage
from utils.tracing import playwright_trace


@pytest.mark.parametrize(
    "action, expected_status",
    [
        ("Reject", "Rejected"),
        ("Shortlist", "Shortlisted"),
    ],
    ids=["reject-by-hiring-manager", "shortlist-by-hiring-manager"],
)
@playwright_trace()
def test_hiring_manager_can_update_candidate_application_stage(
    page,
    request,
    vacancy_factory,
    candidate_factory,
    action,
    expected_status,
):
    _ = (page, request)
    vacancy_data = build_vacancy_data(VACANCY_CASES[0])
    created_vacancy = vacancy_factory(vacancy_data)
    candidate_data = build_candidate_data(created_vacancy["vacancy_name"])
    created_candidate = candidate_factory(candidate_data)

    CandidatesPage(created_candidate["page"]).change_application_stage(
        action, expected_status
    )
