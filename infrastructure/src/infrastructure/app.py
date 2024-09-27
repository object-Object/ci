import logging

import aws_cdk as cdk

from object_ci.aws_cdk.constants import PROD_ENVIRONMENT
from object_ci.logging import setup_logging

from .stack import CIRepository, Stack

logger = logging.getLogger(__name__)


def main():
    setup_logging()

    logger.info("Ready.")
    app = cdk.App()

    Stack(
        app,
        "prod",
        env=PROD_ENVIRONMENT,
        repos=[
            CIRepository(
                owner="object-Object",
                repo="ci",
                github_environment="aws-cdk",
            ),
            CIRepository(
                owner="object-Object",
                repo="discord-github-utils",
                github_environment="prod-aws-cdk",
            ),
        ],
    )

    logger.info("Synthesizing.")
    app.synth()


if __name__ == "__main__":
    main()
