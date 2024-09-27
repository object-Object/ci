import logging
from typing import Any

import aws_cdk as cdk
import aws_cdk_github_oidc as github_oidc
from constructs import Construct

from object_ci.types import GitHubRepository

logger = logging.getLogger(__name__)


class BaseStack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        stage: str,
        *,
        env: cdk.Environment,
        github_repo: GitHubRepository | None = None,
        base_stack_name: str | None = None,
        **kwargs: Any,
    ):
        if github_repo is None:
            github_repo = GitHubRepository.from_env()
        if base_stack_name is None:
            base_stack_name = github_repo.repo

        stack_name = f"{stage}-{base_stack_name}"
        logger.info(f"Initializing stack: {stack_name}")
        super().__init__(
            scope,
            id=stage,
            stack_name=stack_name,
            env=env,
            **kwargs,
        )
        self.github_repo = github_repo
        self.base_stack_name = base_stack_name

        # common external resources

        self.oidc_proxy = github_oidc.GithubActionsIdentityProvider.from_account(
            self,
            "GitHubOIDCProviderProxy",
        )
