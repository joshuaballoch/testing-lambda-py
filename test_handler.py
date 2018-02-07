import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_s3
from handler import call

BUCKET = "some-bucket"
KEY = "incoming/transaction-0001.txt"
BODY = "Hello World!"

## Test Setup Functions

from contextlib import contextmanager

@contextmanager
def do_test_setup():
    with mock_s3():
        set_up_s3()
        yield

def set_up_s3():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=BUCKET)
    boto3.client('s3', region_name='us-east-1').put_object(Bucket=BUCKET, Key=KEY, Body=BODY)

## Tests

def test_handler_moves_incoming_object_to_processed():
    with do_test_setup():
        # Run call with an event describing the file:
        call(s3_object_created_event(BUCKET, KEY), None)

        conn = boto3.resource('s3', region_name='us-east-1')
        # Assert the original file doesn't exist
        with pytest.raises(ClientError) as e_info:
            conn.Object(BUCKET, KEY).get()
            assert e_info.response['Error']['Code'] == 'NoSuchKey'

        # Check that it exists in `processed/`
        obj = conn.Object(BUCKET, "processed/transaction-0001.txt").get()
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
