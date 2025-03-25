from dataclasses import dataclass

from aws_cdk import Environment
from aws_cdk.aws_iam import Role
from aws_cdk_github_oidc import GithubActionsRole
from constructs import Construct

from object_ci.aws_cdk.base_stack import BaseStack
from object_ci.types import GitHubRepository


@dataclass(kw_only=True)
class GitHubEnvironment(GitHubRepository):
    github_environment: str


class Stack(BaseStack):
    def __init__(
        self,
        scope: Construct,
        stage: str,
        *,
        env: Environment,
        repos: list[GitHubEnvironment],
    ):
        super().__init__(
            scope,
            stage,
            env=env,
        )

        cdk_role_proxy = Role.from_role_arn(
            self,
            "CDKRoleProxy",
            f"arn:aws:iam::{self.account}:role/cdk-*",
        )

        for repo in repos:
            role = GithubActionsRole(
                self,
                f"ActionsCDKRole/{repo.owner}/{repo.repo}",
                role_name=f"{stage}ActionsCDK@{repo.owner}+{repo.repo}",
                provider=self.oidc_proxy,
                owner=repo.owner,
                repo=repo.repo,
                filter=f"environment:{repo.github_environment}",
            )
            cdk_role_proxy.grant_assume_role(role)
