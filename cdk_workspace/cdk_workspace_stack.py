from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
import aws_cdk.aws_ecr_assets as ecr_assets
from constructs import Construct
import aws_cdk.aws_ecr as ecr
import os
import aws_cdk.aws_apprunner as apprunner


class CdkWorkspaceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Assuming you have already created an ECR repository and uploaded an image
        repository = ecr.Repository(
            self,
            "MyRepository",
            repository_name="my-repo-name",
        )

        # Assuming you have already created a DockerImageAsset
        asset = ecr_assets.DockerImageAsset(
            self,
            "MyDockerImage",
            directory=os.path.join(os.path.dirname(__file__), ".."),
            file="Dockerfile",
        )

        # Create an App Runner service
        service = apprunner.CfnService(
            self,
            "MyAppRunnerService",
            source_configuration=apprunner.CfnService.SourceConfigurationProperty(
                authentication_configuration=apprunner.CfnService.AuthenticationConfigurationProperty(
                    access_role_arn="arn:aws:iam::251265884217:role/service-role/AppRunnerECRAccessRole",
                    # connection_arn="connectionArn",
                ),
                image_repository=apprunner.CfnService.ImageRepositoryProperty(
                    image_identifier=asset.image_uri,  # Use the image URI from the DockerImageAsset
                    image_repository_type="ECR",
                    image_configuration=apprunner.CfnService.ImageConfigurationProperty(
                        port="80",
                    ),
                ),
            ),
            # instance_configuration=apprunner.CfnService.InstanceConfigurationProperty(
            #     cpu="1024",
            #     memory="2",
            #     instance_role_arn="arn:aws:iam::123456789012:role/MyInstanceRole",  # Replace with your instance role ARN
            # ),
            # auto_scaling_configuration_arn="arn:aws:apprunner:us-east-1:123456789012:autoscalingconfiguration/high-availability/3",  # Adjust as necessary
            service_name="MyAppRunnerServiceName",  # Unique name for your service
        )
