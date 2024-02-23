from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
import aws_cdk.aws_ecr_assets as ecr_assets
from constructs import Construct
import aws_cdk.aws_ecr as ecr
import os


class CdkWorkspaceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an ECR repository
        repository = ecr.Repository(
            self,
            "MyRepository",
            repository_name="my-repo-name",
        )

        # Build and upload Docker image to ECR
        asset = ecr_assets.DockerImageAsset(
            self,
            "MyDockerImage",
            directory=os.path.join(
                os.path.dirname(__file__), ".."
            ),  # Adjust the path as necessary
            file="Dockerfile",  # Specify the Dockerfile name
        )
