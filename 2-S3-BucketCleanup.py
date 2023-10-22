import boto3
from datetime import datetime, timedelta
def lambda_handler(event, context):
    # Initialize an S3 client
    s3 = boto3.client('s3')
    # Specify the S3 bucket name
    bucket_name = 'revanth.k'
    # Calculate the date 30 days ago
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
    # List objects in the S3 bucket
    objects = s3.list_objects_v2(Bucket=bucket_name)
    # Initialize a list to store the names of deleted objects
    deleted_objects = []
    # Iterate through objects and delete files older than 30 days
    for obj in objects.get('Contents', []):
        last_modified = obj['LastModified']
        if last_modified.isoformat() < thirty_days_ago:
            # Delete the object
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
            deleted_objects.append(obj['Key'])
    # Print the names of deleted objects for logging purposes
    if deleted_objects:
        print(f"Deleted objects in {bucket_name}:\n{', '.join(deleted_objects)}")
    else:
        print("No objects were deleted.")
        
    return {
        'statusCode': 200,
        'body': 'Files older than 30 days were deleted'
    }