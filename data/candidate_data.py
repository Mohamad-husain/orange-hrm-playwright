from dataclasses import dataclass

from faker import Faker


fake = Faker()


@dataclass(frozen=True)
class CandidateData:
    """Generated candidate data used by recruitment tests."""

    first: str
    middle: str
    last: str
    email: str
    vacancy_name: str

    @property
    def full_name(self):
        return " ".join((self.first, self.middle, self.last))


def build_candidate_data(vacancy_name):
    return CandidateData(
        first=fake.first_name(),
        middle=fake.first_name(),
        last=fake.last_name(),
        email=fake.unique.email(),
        vacancy_name=vacancy_name,
    )
