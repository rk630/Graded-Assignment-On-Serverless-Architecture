import boto3

def lambda_handler(event, context):
    # Specify the ELB name
    elb_name = 'arn:aws:elasticloadbalancing:ap-south-1:295397358094:targetgroup/rk-targetgroup/1faa693b2f91c277'
    # Initialize an ELB client
    elb_client = boto3.client('elbv2')
    # Initialize an SNS client
    sns_client = boto3.client('sns')
    # Describe the instances registered with the ELB
    response = elb_client.describe_target_health(TargetGroupArn=elb_name)
    # Check the health status of each registered instance
    unhealthy_instances = [instance for instance in response['TargetHealthDescriptions'] if instance['TargetHealth']['State'] != 'healthy']
    if unhealthy_instances:
        # If there are unhealthy instances, publish a message to an SNS topic
        sns_topic_arn = 'arn:aws:sns:ap-south-1:295397358094:rk_sns'
        message = f"The following instances behind ELB {elb_name} are unhealthy: {unhealthy_instances}"
        print(message)
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject="ELB Unhealthy Instances"
        )