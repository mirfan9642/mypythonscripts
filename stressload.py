import psutil
import time

def memory_stress_to_85(duration=10):
    mem = psutil.virtual_memory()
    total_mb = mem.total // (1024 * 1024)
    used_mb = mem.used // (1024 * 1024)
    
    target_usage_mb = int(total_mb * 0.85)
    allocate_mb = target_usage_mb - used_mb
    
    if allocate_mb <= 0:
        print("Memory usage is already above 85%")
        return
    
    block_size = 1 * 1024 * 1024  # 1 MB per block
    
    print(f"Total memory: {total_mb} MB")
    print(f"Current used memory: {used_mb} MB")
    print(f"Allocating ~{allocate_mb} MB to reach ~85% memory usage")
    
    a = ['X' * block_size for _ in range(allocate_mb)]
    
    print(f"Holding allocated memory for {duration} seconds...")
    time.sleep(duration)
    
    del a
    print("Memory released.")

if __name__ == "__main__":
    memory_stress_to_85()

