from aws_cdk import core as cdk
import os
import os.path
# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk import (core, aws_ec2 as ec2, aws_ecs as ecs,
					 aws_ecs_patterns as ecs_patterns,
					 aws_ecr as ecr, aws_route53 as r53, aws_certificatemanager as acm)
from aws_cdk.aws_ecr_assets import DockerImageAsset

dirname = os.path.dirname(__file__)


class SampleAwsEcsPhpAppStack(cdk.Stack):

	def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

        # create Docker image from Dockerfile in below directory
		dockerimage = DockerImageAsset(self, "php8-apache-image",directory=os.path.join(dirname, "php-app"))

		# uncomment and set enviornment variables to use Route53 Public Hosted Zone & ACM Certificate
        #zone = r53.PublicHostedZone.from_lookup(self, 'existing-zone',domain_name=os.getenv('CDK_DOMAIN_NAME'))
		#cert = acm.Certificate.from_certificate_arn(self,'existing-cert',os.getenv('CDK_CERT_ARN'))

		# Create VPC with Isolated + Public subnets
        
		vpc = ec2.Vpc(self, "php-app-vpc", max_azs=3,
			subnet_configuration=[
				ec2.SubnetConfiguration(name="public-subnet",subnet_type=ec2.SubnetType.PUBLIC),
				ec2.SubnetConfiguration(name="isolated-subnet",subnet_type=ec2.SubnetType.ISOLATED),
	      		],
			gateway_endpoints={
				"S3": ec2.GatewayVpcEndpointOptions(service=ec2.GatewayVpcEndpointAwsService.S3)
			},
			enable_dns_hostnames=True,
			enable_dns_support=True,
		)     


		# ECR Endpoint
		ecr_endpoint = ec2.InterfaceVpcEndpoint(
			self, 'EcrEndpoint',
			vpc=vpc,
			open=True,
			service=ec2.InterfaceVpcEndpointAwsService.ECR,
		)


		# ECR Docker Endpoint	
	

		ecr__dkr_endpoint = ec2.InterfaceVpcEndpoint(
			self, 'EcrDockerEndpoint',
			vpc=vpc,
			open=True,
			service=ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER,
		)



		# CloudWatch Logs Endpoint

		cw_logs_endpoints = ec2.InterfaceVpcEndpoint(
			self, 'CloudWatchLogsEndpoint',
			vpc=vpc,
			open=True,
			service=ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_LOGS,
		)


		cluster = ecs.Cluster(self, "php-app-cluster", vpc=vpc)

		ecs_patterns.ApplicationLoadBalancedFargateService(self, "php-app",
			cluster=cluster,            # Required
            listener_port=80,
#           listener_port=443,
#			domain_name=os.getenv('CDK_FQDN'),
#			domain_zone=zone,
#			certificate=cert,
			cpu=256,                    # Default is 256
			desired_count=1,            # Default is 1
			assign_public_ip=False,		# Default is False
			task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
			image=ecs.ContainerImage.from_docker_image_asset(dockerimage)),
			memory_limit_mib=512,      # Default is 512
			public_load_balancer=True)  # Default is False



