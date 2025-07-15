import boto3
from botocore.exceptions import ClientError
import time

def publish_sns_message(topic_arn, message, subject=None):
    sns_client = boto3.client('sns')
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject if subject else ''
        )
        print(f"Message published. MessageId: {response['MessageId']}")
    except ClientError as e:
        print(f"Failed to publish message: {e}")

def run_task_and_notify(topic_arn):
    print("Starting some task...")
    
    # Simulate a task (e.g., memory stress or CPU stress)
    time.sleep(10)  # replace with your actual task
    
    # Task completed — send notification
    publish_sns_message(
        topic_arn,
        message="Task completed successfully.",
        subject="Task Status"
    )

if __name__ == "__main__":
    # Your SNS topic ARN here
    topic_arn = 'arn:aws:sns:us-east-1:123456789012:MyTopic'
    
    # Run the task and notify when done
    run_task_and_notify(topic_arn)

