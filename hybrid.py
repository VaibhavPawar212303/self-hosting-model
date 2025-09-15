import psutil
import time

try:
    import pynvml
    pynvml.nvmlInit()
    gpu_available = True
except:
    gpu_available = False

def get_cpu_info():
    cpu_percent = psutil.cpu_percent(interval=1)  # overall CPU %
    cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)  # core-wise usage
    return cpu_percent, cpu_per_core

def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "total": round(mem.total / (1024 ** 3), 2),  # in GB
        "available": round(mem.available / (1024 ** 3), 2),
        "used": round(mem.used / (1024 ** 3), 2),
        "percent": mem.percent
    }

def get_gpu_info():
    if not gpu_available:
        return None
    gpu_info_list = []
    device_count = pynvml.nvmlDeviceGetCount()
    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        name = pynvml.nvmlDeviceGetName(handle).decode("utf-8")
        memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        gpu_info_list.append({
            "name": name,
            "memory_total": round(memory.total / (1024 ** 3), 2),
            "memory_used": round(memory.used / (1024 ** 3), 2),
            "memory_free": round(memory.free / (1024 ** 3), 2),
            "utilization_gpu": utilization.gpu,
            "utilization_mem": utilization.memory
        })
    return gpu_info_list

if __name__ == "__main__":
    while True:
        cpu_percent, cpu_per_core = get_cpu_info()
        mem_info = get_memory_info()
        gpu_info = get_gpu_info()

        print("="*40)
        print(f"CPU Usage: {cpu_percent}%")
        for idx, usage in enumerate(cpu_per_core):
            print(f"  Core {idx}: {usage}%")

        print(f"Memory: {mem_info['used']} GB used / {mem_info['total']} GB total "
              f"({mem_info['percent']}%)")

        if gpu_info:
            for gpu in gpu_info:
                print(f"GPU: {gpu['name']}")
                print(f"  Memory Used: {gpu['memory_used']} GB / {gpu['memory_total']} GB")
                print(f"  GPU Utilization: {gpu['utilization_gpu']}% | "
                      f"Memory Utilization: {gpu['utilization_mem']}%")
        else:
            print("GPU: Not Available on this machine.")

        time.sleep(3)
