import boto3
from botocore.exceptions import ClientError
import time
import psutil  # Make sure to install with: pip install psutil

def publish_sns_message(topic_arn, message, subject=None):
    sns_client = boto3.client('sns', region_name='ap-south-1')  # or your region
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject if subject else 'System Alert'
        )
        print(f"✅ Message published. MessageId: {response['MessageId']}")
    except ClientError as e:
        print(f"❌ Failed to publish message: {e}")

def run_task_and_notify(topic_arn):
    print("🟢 Starting task and monitoring system...")

    alert_sent = False
    start_time = time.time()
    duration = 30  # seconds — simulate your actual task duration
    while time.time() - start_time < duration:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent

        print(f"📊 CPU: {cpu_usage}% | Memory: {memory_usage}%")

        if (cpu_usage > 80 or memory_usage > 80) and not alert_sent:
            publish_sns_message(
                topic_arn,
                message=f"⚠️ High resource usage detected!\nCPU: {cpu_usage}%\nMemory: {memory_usage}%",
                subject="🚨 High CPU/Memory Alert"
            )
            alert_sent = True

        time.sleep(1)

    # ✅ This part is outside the while loop
    if alert_sent:
        publish_sns_message(
            topic_arn,
            message="You have used more than 80% of memory or CPU Freeup or Clear Your memory or CPU .",
            subject="High Usage Alert"
        )
    else:
        publish_sns_message(
            topic_arn,
            message="Task completed successfully. CPU and memory usage stayed under 80%.",
            subject="Normal Usage"
        )

    print("🖥️ Monitoring CPU Memory Completed. Check your email.")

if __name__ == "__main__":
    # Paste your actual SNS topic ARN below
    topic_arn = 'arn:aws:sns:ap-south-1:325511643680:stress'
    
    run_task_and_notify(topic_arn)

