from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class VacancyData:
    """Vacancy data used by recruitment setup tests and fixtures."""

    name: str
    job_title: str
    description: str
    hiring_manager_hint: str
    hiring_manager: str
    positions: str
    active: bool


VACANCY_CASES = [
    VacancyData(
        name="Senior QA Engineer",
        job_title="QA Engineer",
        description="Owns manual and automation coverage for product releases.",
        hiring_manager_hint="pe",
        hiring_manager="Peter Mac Anderson",
        positions="2",
        active=True,
    ),
    VacancyData(
        name="Senior IT Manager",
        job_title="IT Manager",
        description="Leads infrastructure operations and incident management.",
        hiring_manager_hint="pe",
        hiring_manager="Peter Mac Anderson",
        positions="1",
        active=False,
    ),
    VacancyData(
        name="software engineering",
        job_title="Software Engineer",
        description="Builds and maintains application features across product teams.",
        hiring_manager_hint="pe",
        hiring_manager="Peter Mac Anderson",
        positions="3",
        active=True,
    ),
]


def build_vacancy_data(vacancy_case):
    return asdict(vacancy_case)
