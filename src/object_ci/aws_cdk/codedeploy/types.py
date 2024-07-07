from dataclasses import dataclass

from typing_extensions import override

from object_ci.utils import getenv_or_raise


@dataclass
class GitHubRepository:
    owner: str
    repo: str

    @classmethod
    def from_env(cls, key: str = "GITHUB_REPOSITORY"):
        value = getenv_or_raise(key)
        if "/" not in value:
            raise ValueError(
                f"Invalid value for envvar {key} (does not contain '/'): {value}"
            )
        owner, repo = value.split("/", maxsplit=1)
        return cls(owner=owner, repo=repo)

    @override
    def __str__(self):
        return f"{self.owner}/{self.repo}"
