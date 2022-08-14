from constructs import Construct
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_aws import AwsProvider, s3
from cdktf_cdktf_provider_aws.s3 import S3BucketAcl
from cdktf_cdktf_provider_azurerm import AzurermProvider, DataAzurermResourceGroup, StorageAccount


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        # define resources here
        super().__init__(scope, ns)
        AwsProvider(self, "AWS", region="ap-southeast-2")
        AzurermProvider(self, "AzureRm", features={},
                        skip_provider_registration=True)
        defaultRg = DataAzurermResourceGroup(
            self, "testrg", name="rg-aurelz-sandbox")
        StorageAccount(self, "suhantestsa", name="suhantestsa", resource_group_name=defaultRg.name,
                       location=defaultRg.location, account_tier="Standard", account_replication_type="LRS")
        s3Bucket = s3.S3Bucket(self, "tests3", bucket="suhan-cdktf-test-s3")
        S3BucketAcl(self, "bucketacl", bucket=s3Bucket.id, acl="private")


app = App()
MyStack(app, "suhan-cdktf-python-demo-app")
app.synth()
