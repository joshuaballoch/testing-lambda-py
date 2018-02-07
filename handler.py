import boto3
import re

def move_object_to_processed(s3_client, original_bucket, original_key):
    new_key = re.sub("incoming\/", "processed/", original_key)
    s3_client.copy_object(
        Bucket=original_bucket,
        Key=new_key,
        CopySource={'Bucket': original_bucket, 'Key': original_key}
    )
    s3_client.delete_object(Bucket=original_bucket, Key=original_key)

def call(event, context):
    s3_client = boto3.client('s3')
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    move_object_to_processed(s3_client, bucket, key)
