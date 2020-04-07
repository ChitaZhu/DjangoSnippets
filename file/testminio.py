# Import MinIO library.
import json
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
from argparse import ArgumentError

# Initialize minioClient with an endpoint and access/secret keys.
minioClient = Minio('192.168.31.122:9000',
                    access_key='minioadmin',
                    secret_key='minioadmin',
                    secure=False)

# Make a bucket with the make_bucket API call.
try:
       minioClient.make_bucket("mybucket")
except BucketAlreadyOwnedByYou as err:
       pass
except BucketAlreadyExists as err:
       pass
except ResponseError as err:
       raise

# list_buckets()
buckets = minioClient.list_buckets()
for bucket in buckets:
    print(bucket.name, bucket.creation_date)

# bucket_existes()
try:
    print(minioClient.bucket_exists("mybucket"))
except ResponseError as err:
    print(err)

# remove_bucket()
# try:
#     minioClient.remove_bucket("mybucket")
# except ResponseError as err:
#     print(err)

# List all object paths in bucket that begin with my-prefixname.
objects = minioClient.list_objects('data1', prefix='data11',
                              recursive=True)
for obj in objects:
    print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
          obj.etag, obj.size, obj.content_type)

# List all object paths in bucket that begin with my-prefixname.
objects = minioClient.list_objects_v2('data1', prefix='data11',
                          recursive=True, start_after='data11')
for obj in objects:
    print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
          obj.etag, obj.size, obj.content_type)

# List all object paths in bucket that begin with my-prefixname.
uploads = minioClient.list_incomplete_uploads('data1',
                                         prefix=None,
                                         recursive=True)
for obj in uploads:
    print("======================================================")
    print(obj.bucket_name, obj.object_name, obj.upload_id, obj.size)

# Set bucket policy to read only to all object paths in bucket.
policy_read_only = {"Version":"2012-10-17",
                    "Statement":[
                        {
                        "Sid":"",
                        "Effect":"Allow",
                        "Principal":{"AWS":"*"},
                        "Action":"s3:GetBucketLocation",
                        "Resource":"arn:aws:s3:::mybucket"
                        },
                        {
                        "Sid":"",
                        "Effect":"Allow",
                        "Principal":{"AWS":"*"},
                        "Action":"s3:ListBucket",
                        "Resource":"arn:aws:s3:::mybucket"
                        },
                        {
                        "Sid":"",
                        "Effect":"Allow",
                        "Principal":{"AWS":"*"},
                        "Action":"s3:GetObject",
                        "Resource":"arn:aws:s3:::mybucket/*"
                        }
                    ]}

minioClient.set_bucket_policy('mybucket', json.dumps(policy_read_only))

# Get current policy of all object paths in bucket "mybucket".
policy = minioClient.get_bucket_policy('mybucket')
print(policy)

notification = {
    'QueueConfigurations': [
        {
            'Id': '1',
            'Arn': 'arn1',
            'Events': ['s3:ObjectCreated:*'],
            'Filter': {
                'Key': {
                    'FilterRules': [
                        {
                            'Name': 'prefix',
                            'Value': 'abc'
                        }
                    ]
                }
            }
        }
    ],
    'TopicConfigurations': [
        {
            'Arn': 'arn2',
            'Events': ['s3:ObjectCreated:*'],
            'Filter': {
                'Key': {
                    'FilterRules': [
                        {
                            'Name': 'suffix',
                            'Value': '.jpg'
                        }
                    ]
                }
            }
        }
    ],
    'CloudFunctionConfigurations': [
        {
            'Arn': 'arn3',
            'Events': ['s3:ObjectRemoved:*'],
            'Filter': {
                'Key': {
                    'FilterRules': [
                        {
                            'Name': 'suffix',
                            'Value': '.jpg'
                        }
                    ]
                }
            }
        }
    ]
}

# try:
#     minioClient.set_bucket_notification('mybucket', notification)
# except ResponseError as err:
#     # handle error response from service.
#     print(err)
# except (ArgumentError, TypeError) as err:
#     # should happen only during development. Fix the notification argument
#     print(err)


# # Get the notifications configuration for a bucket.
# notification = minioClient.get_bucket_notification('mybucket')
# print("============:{}".format(notification))
# # If no notification is present on the bucket:
# # notification == {}

# Sample default encryption configuration
# ENC_CONFIG = {
#     'ServerSideEncryptionConfiguration':{
#         'Rule': [
#             {'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}
#         ]
#     }
# }
# try:
#     minioClient.put_bucket_encryption('mybucket', ENC_CONFIG)
# except ResponseError as err:
#     print(err)

# # Get the default encryption configuration set on bucket, "mybucket".
# encryption = minioClient.get_bucket_encryption('mybucket')
# print(encryption)

# Get a full object.
try:
    data = minioClient.get_object('mybucket', 'xxxx工程进度-旭日图.png')
    with open('my-testfile', 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
except ResponseError as err:
    print(err)

# Put an object 'pumaserver_debug.log' with contents from 'pumaserver_debug.log'.
# try:
#        minioClient.fput_object('maylogs', 'pumaserver_debug.log', r'D:\workspace\zhuxudan\mysite\file\images\xxxx工程进度.png')
# except ResponseError as err:
#        print(err)

# try:
#     print(minioClient.fget_object('maylogs', 'pumaserver_debug.log', r'D:\workspace\zhuxudan\mysite\file\xxxx工程进度.png'))
# except ResponseError as err:
#     print(err)