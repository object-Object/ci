import logging

import aws_cdk as cdk
import aws_cdk_github_oidc as github_oidc
from aws_cdk import (
    aws_codedeploy as codedeploy,
    aws_iam as iam,
    aws_s3 as s3,
)
from constructs import Construct

from object_ci.aws_cdk.constants import (
    PROD_ACCOUNT,
    PROD_ARTIFACTS_BUCKET_NAME,
    PROD_CODEDEPLOY_ENVIRONMENT,
    PROD_REGION,
    PROD_VULTR_VPS_INSTANCE_TAG,
)

from .types import GitHubRepository

logger = logging.getLogger(__name__)


class CodeDeployStack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        stage: str,
        *,
        base_stack_name: str,
        github_repo: GitHubRepository,
        env: cdk.Environment,
        artifacts_bucket: str | s3.IBucket,
        codedeploy_environment: str,
        on_premise_instance_tag: str,
    ):
        stack_name = f"{stage}-{base_stack_name}"
        logger.info(f"Initializing stack: {stack_name}")
        super().__init__(
            scope,
            id=stage,
            stack_name=stack_name,
            env=env,
        )

        self.on_premise_instance_tag = on_premise_instance_tag

        # external resources

        self.oidc_proxy = github_oidc.GithubActionsIdentityProvider.from_account(
            self,
            "GitHubOIDCProviderProxy",
        )

        self.artifacts_bucket_proxy: s3.IBucket
        match artifacts_bucket:
            case str() as artifacts_bucket_name:
                self.artifacts_bucket_proxy = s3.Bucket.from_bucket_name(
                    self,
                    "ArtifactsBucketProxy",
                    artifacts_bucket_name,
                )
            case _:
                self.artifacts_bucket_proxy = artifacts_bucket

        # CodeDeploy

        self.application = codedeploy.ServerApplication(self, "Application")

        self.deployment_group = self.create_deployment_group()

        # GitHub Actions

        self.actions_role = github_oidc.GithubActionsRole(
            self,
            "ActionsCodeDeployRole",
            provider=self.oidc_proxy,
            owner=github_repo.owner,
            repo=github_repo.repo,
            filter=f"environment:{codedeploy_environment}",
        )
        self.artifacts_bucket_proxy.grant_read_write(self.actions_role)
        self.actions_role.add_to_policy(
            iam.PolicyStatement(
                actions=["codedeploy:*"],
                resources=[
                    self.application.application_arn,
                    self.deployment_group.deployment_group_arn,
                    self.deployment_config.deployment_config_arn,
                ],
            )
        )

        # outputs

        cdk.CfnOutput(
            self,
            "ApplicationName",
            value=self.application.application_name,
        )
        cdk.CfnOutput(
            self,
            "DeploymentGroupName",
            value=self.deployment_group.deployment_group_name,
        )
        cdk.CfnOutput(
            self,
            "ActionsCodeDeployRoleARN",
            value=self.actions_role.role_arn,
        )
        cdk.CfnOutput(
            self,
            "ArtifactsBucketName",
            value=self.artifacts_bucket_proxy.bucket_name,
        )

    @property
    def deployment_config(self) -> codedeploy.ServerDeploymentConfig:
        return codedeploy.ServerDeploymentConfig.ONE_AT_A_TIME

    @property
    def auto_rollback_config(self) -> codedeploy.AutoRollbackConfig:
        return codedeploy.AutoRollbackConfig(
            failed_deployment=True,
        )

    @property
    def on_premise_instance_tags(self) -> codedeploy.InstanceTagSet:
        return codedeploy.InstanceTagSet({
            "instance": [self.on_premise_instance_tag],
        })

    def create_deployment_group(self):
        return codedeploy.ServerDeploymentGroup(
            self,
            "DeploymentGroup",
            application=self.application,
            deployment_config=self.deployment_config,
            auto_rollback=self.auto_rollback_config,
            on_premise_instance_tags=self.on_premise_instance_tags,
        )

    @classmethod
    def default_prod_stack(
        cls,
        scope: Construct,
        stage: str = "prod",
        *,
        base_stack_name: str,
        github_repo: GitHubRepository | None = None,
        on_premise_instance_tag: str = PROD_VULTR_VPS_INSTANCE_TAG,
    ):
        return cls(
            scope,
            stage,
            base_stack_name=base_stack_name,
            github_repo=github_repo or GitHubRepository.from_env(),
            env=cdk.Environment(
                account=PROD_ACCOUNT,
                region=PROD_REGION,
            ),
            artifacts_bucket=PROD_ARTIFACTS_BUCKET_NAME,
            codedeploy_environment=PROD_CODEDEPLOY_ENVIRONMENT,
            on_premise_instance_tag=on_premise_instance_tag,
        )
