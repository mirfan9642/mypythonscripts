import psutil, time

def memory_stress_safe(duration=90, usage_fraction=0.3):
    print("Starting memory stress test...")
    size = int(psutil.virtual_memory().total * usage_fraction)
    print(f"Allocating ~{size / (1024*1024):.0f} MB")
    block = 'X' * (1024 * 1024)
    a = [block] * (size // (1024 * 1024))
    time.sleep(duration)
    del a
    print("Memory stress test complete.")

if __name__ == "__main__":
    memory_stress_safe(duration=90, usage_fraction=0.85)

