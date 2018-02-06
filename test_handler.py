import boto3
import pytest
from botocore.exceptions import ClientError
from handler import call
from moto import mock_s3

BUCKET = "some-bucket"
KEY = "incoming/transaction-0001.txt"
BODY = "Hello All!"
TXNS_TABLE = "my-transactions-table"

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
        call(s3_object_created_event(BUCKET, KEY), None)

        conn = boto3.resource('s3', region_name='us-east-1')
        assert_object_doesnt_exist(conn, BUCKET, KEY)
        obj = conn.Object(BUCKET, "processed/transaction-0001.txt").get()
        assert obj['Body'].read() == b'Hello All!'

## Helpers

def assert_object_doesnt_exist(conn, bucket_name, key):
    with pytest.raises(ClientError) as e_info:
        conn.Object(bucket_name, key).get()
        assert e_info.response['Error']['Code'] == 'NoSuchKey'

def s3_object_created_event(bucket_name, key):
    return {
      "Records": [
        {
          "eventVersion": "2.0",
          "eventTime": "1970-01-01T00:00:00.000Z",
          "requestParameters": {
            "sourceIPAddress": "127.0.0.1"
          },
          "s3": {
            "configurationId": "testConfigRule",
            "object": {
              "eTag": "0123456789abcdef0123456789abcdef",
              "sequencer": "0A1B2C3D4E5F678901",
              "key": key,
              "size": 1024
            },
            "bucket": {
              "arn": "bucketarn",
              "name": bucket_name,
              "ownerIdentity": {
                "principalId": "EXAMPLE"
              }
            },
            "s3SchemaVersion": "1.0"
          },
          "responseElements": {
            "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH",
            "x-amz-request-id": "EXAMPLE123456789"
          },
          "awsRegion": "us-east-1",
          "eventName": "ObjectCreated:Put",
          "userIdentity": {
            "principalId": "EXAMPLE"
          },
          "eventSource": "aws:s3"
        }
      ]
    }

