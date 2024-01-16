from moto import mock_s3,mock_dynamodb
import pytest
import boto3
import os

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture(scope="function")
def s3(aws_credentials):
    with mock_s3():
        yield boto3.client("s3", region_name="us-east-1")

@pytest.fixture
def create_bucket1(s3):
    boto3.client("s3").create_bucket(Bucket="b-one")

@pytest.fixture
def create_bucket2(s3):
    boto3.client("s3").create_bucket(Bucket="b-two")

def test_s3_directly(s3):
    s3.create_bucket(Bucket="somebucket")

    result = s3.list_buckets()
    assert len(result["Buckets"]) == 1

def test_bucket_creation(create_bucket1, create_bucket2):
    buckets = boto3.client("s3").list_buckets()["Buckets"]
    assert len(buckets) == 2