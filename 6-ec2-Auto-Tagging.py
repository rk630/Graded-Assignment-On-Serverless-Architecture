import json, boto3
from datetime import datetime

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')

    # Get instance details from the Event
    instance_id = event['detail']['instance-id']
    instance_state = event['detail']['state']

    if instance_state == 'running':
        # Get the instance
        instance = ec2.Instance(instance_id)

        # Create tags
        tags = [
            {
                'Key': 'LaunchDate',
                'Value': str(datetime.now())
            },
            {
                'Key': 'Purpose',
                'Value': 'indefinite purpose'  # replace with your custom value
            }
        ]

        # Add tags to the instance
        instance.create_tags(Tags=tags)

    return {
        'statusCode': 200,
        'body': json.dumps('Tags added to the EC2 instance!')
    }