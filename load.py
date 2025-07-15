import psutil, time

def memory_stress_safe(duration=30, usage_fraction=0.5):
    print(f"🧠 Using ~{usage_fraction*100:.0f}% memory for {duration}s...")
    size = int(psutil.virtual_memory().total * usage_fraction)
    block = 'X' * (1024 * 1024)  # 1 MB
    a = [block] * (size // (1024 * 1024))
    time.sleep(duration)
    del a
    print("✅ Done.")



