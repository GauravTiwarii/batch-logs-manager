import os
import pytest
import boto3

from moto import mock_s3

Event = {
    "Records": [{
        "s3": {
            'bucket': {'name': 'batch-logs-2021'},
            'object': {
                'key': 'file1.csv'
            }
        }
    }]
}


@pytest.fixture
def aws_config():
    # mocked aws credentials
    os.environ["AWS_ACCESS_KEY_ID"] = "mocked"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "mocked"


@pytest.fixture
def s3_client():
    with mock_s3():
        s3_client = boto3.client("s3", region_name="eu-west-1")
        yield s3_client
