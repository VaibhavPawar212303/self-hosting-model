import requests
import time

CPU_TOTAL_API = "http://localhost:61208/api/4/cpu"
CPU_CORE_API = "http://localhost:61208/api/4/cpu/core"
GPU_API = "http://localhost:61208/api/4/gpu"
TIMEOUT = 10
SLEEP = 2

while True:
    try:
        # --- CPU TOTAL ---
        cpu_total = requests.get(CPU_TOTAL_API, timeout=TIMEOUT).json()
        total = cpu_total.get("total", 0.0)
        user = cpu_total.get("user", 0.0)
        system = cpu_total.get("system", 0.0)
        idle = cpu_total.get("idle", 0.0)

        print(f"\n[CPU - Total] ({cpu_total.get('cpucore', '?')} cores)")
        print(f"Total: {total:.1f}% | User: {user:.1f}% | System: {system:.1f}% | Idle: {idle:.1f}%")

        # --- CPU PER CORE ---
        try:
            cpu_cores = requests.get(CPU_CORE_API, timeout=TIMEOUT).json()
            if isinstance(cpu_cores, list) and cpu_cores:
                print("[CPU - Per Core]")
                for idx, usage in enumerate(cpu_cores):
                    print(f"Core {idx}: {usage:.1f}%")
            else:
                print(f"Core {idx}: {usage:.1f}%")
        except Exception as e:
            print(f"[CPU - Per Core] Error: {e}")

        # --- GPU ---
        try:
            gpu_stats = requests.get(GPU_API, timeout=TIMEOUT).json()
            if gpu_stats:
                print("[GPU]")
                for idx, gpu in enumerate(gpu_stats):
                    print(f"GPU {idx}: {gpu.get('gpu_util', 0.0):.1f}% | Mem {gpu.get('mem_util', 0.0):.1f}%")
            else:
                print("[GPU] No GPU detected")
        except Exception:
            print("[GPU] No GPU API available")

    except Exception as e:
        print(f"Unexpected error: {e}")

    time.sleep(SLEEP)
