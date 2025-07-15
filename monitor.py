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
        cpu = psutil.cpu_percent(interval=1)  # waits 1 second
        mem = psutil.virtual_memory().percent
        print(f"📊 CPU: {cpu}% | Memory: {mem}%")

        if (cpu > 60 or mem > 60) and not alert_sent:
            publish_sns_message(
                topic_arn,
                f"⚠️ High resource usage!\nCPU: {cpu}%\nMemory: {mem}%",
                "🚨 High CPU/Memory Alert"
            )
            alert_sent = True

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

def memory_stress_safe(duration=30, usage_fraction=0.85):
    print(f"🧠 Using ~{usage_fraction*100:.0f}% memory for {duration}s...")
    size = int(psutil.virtual_memory().total * usage_fraction)
    block_size = 1024 * 1024  # 1 MB
    blocks = size // block_size

    a = []
    for i in range(blocks):
        a.append(bytearray(b'X' * block_size))
        if i % 50 == 0:
            time.sleep(0.01)  # throttle to avoid OOM kill

    time.sleep(duration)
    del a
    print("🖥️ Monitoring Memory or CPU Completed. Check Email")

if __name__ == "__main__":
    topic_arn = 'arn:aws:sns:ap-south-1:325511643680:stress'

    monitor_thread = threading.Thread(target=run_task_and_notify, args=(topic_arn,))
    monitor_thread.start()

    memory_stress_safe(duration=30, usage_fraction=0.65)

    monitor_thread.join()

