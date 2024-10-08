import aws_cdk as cdk

PROD_ACCOUNT = "511603859520"
PROD_REGION = "us-east-1"
PROD_ENVIRONMENT = cdk.Environment(account=PROD_ACCOUNT, region=PROD_REGION)

PROD_ARTIFACTS_BUCKET_NAME = "prod-objectobject-ca-codedeploy-artifacts"

PROD_CODEDEPLOY_ENVIRONMENT = "prod-codedeploy"
PROD_VULTR_VPS_INSTANCE_TAG = "prod-objectobject-ca"
