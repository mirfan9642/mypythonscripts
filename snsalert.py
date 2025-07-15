import threading
import psutil, time
import boto3
from botocore.exceptions import ClientError

def publish_sns_message(topic_arn, message, subject=None):
    sns_client = boto3.client('sns', region_name='ap-south-1')
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject or 'System Alert'
        )
        print(f"✅ Message sent. ID: {response['MessageId']}")
    except ClientError as e:
        print(f"❌ Failed to send message: {e}")

def run_task_and_notify(topic_arn):
    print("🟢 Monitoring system...")

    alert_sent = False
    start = time.time()
    duration = 30

    while time.time() - start < duration:
        cpu = psutil.cpu_percent(interval=1)  # waits 1 second here
        mem = psutil.virtual_memory().percent
        print(f"📊 CPU: {cpu}% | Memory: {mem}%")

        if (cpu > 80 or mem > 80) and not alert_sent:
            publish_sns_message(
                topic_arn,
                f"⚠️ High resource usage!\nCPU: {cpu}%\nMemory: {mem}%",
                "🚨 High CPU/Memory Alert"
            )
            alert_sent = True
        # no extra time.sleep needed

    if alert_sent:
        publish_sns_message(
            topic_arn,
            "High usage detected during monitoring.",
            "High Usage"
        )
    else:
        publish_sns_message(
            topic_arn,
            "Monitoring completed. Usage stayed below 80%.",
            "Normal Usage"
        )

    print("✅ Monitoring completed.")

def memory_stress_safe(duration=30, usage_fraction=0.5):
    print(f"🧠 Using ~{usage_fraction*100:.0f}% memory for {duration}s...")
    size = int(psutil.virtual_memory().total * usage_fraction)
    block = 'X' * (1024 * 1024)
    a = [block] * (size // (1024 * 1024))
    time.sleep(duration)
    del a
    print("🖥️ Monitoring Memory or Cpu Completed. Check Email")

if __name__ == "__main__":
    topic_arn = 'arn:aws:sns:ap-south-1:325511643680:stress'

    # Start SNS monitoring in a separate thread
    monitor_thread = threading.Thread(target=run_task_and_notify, args=(topic_arn,))
    monitor_thread.start()

    # Start memory stress in main thread
    memory_stress_safe(duration=30, usage_fraction=0.85)

    monitor_thread.join()

