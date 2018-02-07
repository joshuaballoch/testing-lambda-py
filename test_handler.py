import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_s3
from handler import call

## Test Setup Functions

def test_handler_moves_incoming_object_to_processed():
    with mock_s3():
        # Create the bucket
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket="some-bucket")
        # Add a file
        boto3.client('s3', region_name='us-east-1').put_object(Bucket="some-bucket", Key="incoming/transaction-0001.txt", Body="Hello World!")

        # Run call with an event describing the file:
        call(s3_object_created_event("some-bucket", "incoming/transaction-0001.txt"), None)

        # Assert the original file doesn't exist
        with pytest.raises(ClientError) as e_info:
            conn.Object("some-bucket", "incoming/transaction-0001.txt").get()
            assert e_info.response['Error']['Code'] == 'NoSuchKey'

        # Check that it exists in `processed/`
        obj = conn.Object("some-bucket", "processed/transaction-0001.txt").get()
        assert obj['Body'].read() == b'Hello World!'

def s3_object_created_event(bucket_name, key):
    # NOTE: truncated event object shown here
    return {
      "Records": [
        {
          "s3": {
            "object": {
              "key": key,
            },
            "bucket": {
              "name": bucket_name,
            },
          },
        }
      ]
    }


