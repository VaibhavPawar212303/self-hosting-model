import psutil
import time
import json
import requests
import os
import logging
import json
import re
from datetime import datetime
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor

# ================== CONFIG ==================
PROMPTS_FILE = "prompts/prompts.json"
OUTPUT_DIR = "outputs"
MODEL_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b-instruct-q4_K_M"
CPU_LOG_FILE = "cpu_usage.log"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Enable/disable streaming globally
USE_STREAM = True  

# ================== LOGGER SETUP ==================
logging.basicConfig(
    filename=CPU_LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# ================== SYSTEM MONITOR ==================
try:
    import pynvml
    pynvml.nvmlInit()
    gpu_available = True
except Exception:
    gpu_available = False


def get_cpu_info():
    percent = psutil.cpu_percent(interval=0.5)
    per_core = psutil.cpu_percent(interval=0.5, percpu=True)
    logging.info(f"CPU Overall: {percent}%")
    for idx, core in enumerate(per_core):
        logging.info(f"CPU Core {idx}: {core}%")
    return {"overall_percent": percent, "per_core_percent": per_core}


def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "total": round(mem.total / (1024 ** 3), 2),
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


def monitor_system(stop_event, stats_list):
    while not stop_event.is_set():
        stats_list.append({
            "timestamp": datetime.now().isoformat(),
            "cpu": get_cpu_info(),
            "memory": get_memory_info(),
            "gpu": get_gpu_info()
        })
        time.sleep(1)


# ================== STREAM HANDLER ==================
def call_model_streaming(payload):
    """
    Calls Ollama with stream=True and prints chunks live to console,
    while also collecting the full response string.
    """
    response_text = ""
    with requests.post(MODEL_API_URL, json=payload, stream=True, timeout=600) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line.decode("utf-8"))
                chunk = data.get("response", "")
                if chunk:
                    print(chunk, end="", flush=True)  # live stream to console
                    response_text += chunk
            except json.JSONDecodeError:
                continue
    print("\n")  # final newline after stream
    return response_text


# ================== TEXT PARSER ==================
def extract_structured_test_case(text: str):
    split_pattern = r"(?=\*\*?Test Case(?:\s+\d+|:))"
    chunks = re.split(split_pattern, text, flags=re.IGNORECASE)
    cases = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk or not chunk.lower().startswith("**test case"):
            continue

        def extract_section(title, multiline=True):
            pattern = rf"\*\*{title}:?\*\*(.*?)(?=\n\*\*|\Z)"
            match = re.search(pattern, chunk, re.DOTALL | re.IGNORECASE)
            if not match:
                return [] if multiline else None
            content = match.group(1).strip()
            if multiline:
                return [line.strip("-*+•\t ").strip() for line in content.split("\n") if line.strip()]
            return content

        def extract_any(titles, multiline=True):
            for t in titles:
                result = extract_section(t, multiline)
                if result and (result != [] and result is not None):
                    return result
            return [] if multiline else None

        case_data = {
            "test_case": extract_any(["Test Case", "Test Case ID"], multiline=False),
            "objective": extract_any(["Objective", "Test Case Description"], multiline=False),
            "preconditions": extract_any(["Preconditions", "Pre-requisites", "Prerequisites"]),
            "test_data": extract_any(["Test Data"]),
            "test_steps": extract_any(["Test Steps", "Steps", "Procedure"]),
            "expected_results": extract_any(["Expected Results", "Expected Outcome"]),
            "variations": extract_any(["Test Variations", "Test Scenarios", "Test Cases"]),
            "edge_cases": extract_any(["Edge Cases", "Additional Test Cases", "Negative Tests"])
        }
        case_data = {k: v for k, v in case_data.items() if v and v != []}
        cases.append(case_data)
    return cases


# ================== PROMPT LOADER ==================
def load_prompt(version):
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)
    for item in prompts:
        if item["version"] == version:
            return item
    raise ValueError(f"Version {version} not found in {PROMPTS_FILE}")


# ================== PARALLEL MODE ==================
def generate_multiple_test_cases(requirement, version, num_cases=2, use_stream=USE_STREAM):
    prompt_data = load_prompt(version)

    def call_model(case_idx):
        requirement_str = json.dumps(requirement, indent=2)  # ✅ serialize dict to string
        template = prompt_data["template"].replace("{requirement}", requirement_str)
        template += f"\n\n⚡ Generate unique variation #{case_idx+1} of the test cases."
        payload = {"model": MODEL_NAME, "prompt": template, "stream": use_stream}

        if use_stream:
            return call_model_streaming(payload)
        else:
            response = requests.post(MODEL_API_URL, json=payload, timeout=600)
            response.raise_for_status()
            return response.json().get("response", "").strip()

    with ThreadPoolExecutor(max_workers=min(num_cases, os.cpu_count())) as executor:
        outputs = list(executor.map(call_model, range(num_cases)))

    return outputs


# ================== BATCH MODE ==================
def generate_batched_test_cases(requirement, version, use_stream=USE_STREAM):
    prompt_data = load_prompt(version)
    
    requirement_str = json.dumps(requirement, indent=2)  # ✅ serialize dict to string
    template = prompt_data["template"].replace("{requirement}", requirement_str)
    template += f"\n\n⚡ Generate unique test cases in JSON array format. " \
                f"Each item should include: test_case, objective, preconditions, test_data, test_steps, expected_results."

    payload = {
        "model": MODEL_NAME,
        "prompt": template,
        "format": "json",
        "stream": use_stream
    }

    if use_stream:
        return call_model_streaming(payload)
    else:
        response = requests.post(MODEL_API_URL, json=payload, timeout=600)
        response.raise_for_status()
        return response.json().get("response", "").strip()


# ================== MAIN ==================
if __name__ == "__main__":
    requirement = {
        "loginPage": {
            "application": "Scoreboard",
            "powered_by": "Clippd",
            "flow": "Sign in",
            "steps": [
                {
                    "step": 1,
                    "title": "Sign in to Scoreboard",
                    "subtitle": "Welcome back! Please sign in to continue",
                    "options": {
                        "social_login": [
                            {"provider": "Apple", "action": "sign_in_with_apple"},
                            {"provider": "Facebook", "action": "sign_in_with_facebook"},
                            {"provider": "Google", "action": "sign_in_with_google"}
                        ],
                        "email_login": {
                            "field": {
                                "type": "text",
                                "label": "Email address",
                                "placeholder": "Enter your email address",
                                "required": True   # ✅ corrected
                            },
                            "button": {
                                "text": "Continue",
                                "action": "go_to_password_step"
                            }
                        }
                    },
                    "footer": {
                        "signup_prompt": "Don't have an account?",
                        "signup_link": "Sign up",
                        "help_link": "Help",
                        "dev_mode_label": "Development mode"
                    }
                },
                {
                    "step": 2,
                    "title": "Enter your password",
                    "subtitle": "Enter the password associated with your account",
                    "account": "vaibhav.pawar+sb78@clippd.io",
                    "fields": {
                        "password": {
                            "type": "password",
                            "label": "Password",
                            "required": True,   # ✅ corrected
                            "actions": {
                                "forgot_password_link": "Forgot password?",
                                "show_hide_toggle": True   # ✅ corrected
                            }
                        }
                    },
                    "button": {
                        "text": "Continue",
                        "action": "authenticate_user"
                    },
                    "alternatives": {
                        "use_another_method": {
                            "action": "go_to_alternate_methods"
                        }
                    },
                    "footer": {
                        "help_link": "Help",
                        "dev_mode_label": "Development mode"
                    }
                },
                {
                    "step": 3,
                    "title": "Use another method",
                    "subtitle": "Facing issues? You can use any of these methods to sign in.",
                    "options": {
                        "social_login": [
                            {"provider": "Apple", "action": "sign_in_with_apple"},
                            {"provider": "Facebook", "action": "sign_in_with_facebook"},
                            {"provider": "Google", "action": "sign_in_with_google"}
                        ],
                        "email_otp": {
                            "action": "send_email_code",
                            "label": "Email code to vaibhav.pawar+sb78@clippd.io"
                        }
                    },
                    "button": {
                        "text": "Back",
                        "action": "return_to_password_step"
                    },
                    "footer": {
                        "help_link": "Help",
                        "get_help_text": "Don't have any of these? Get help",
                        "dev_mode_label": "Development mode"
                    }
                }
            ]
        }
    }

    version = "v2"
    mode = "batch"   # change to "parallel" or "batch"

    # ====== Start system monitoring in background ======
    stop_event = Event()
    stats_list = []
    monitor_thread = Thread(target=monitor_system, args=(stop_event, stats_list))
    monitor_thread.start()

    try:
        start_time = time.time()  # ✅ start timer

        if mode == "parallel":
            print("📝 Generating multiple test cases in PARALLEL...\n")
            all_outputs = generate_multiple_test_cases(requirement, version, num_cases=2, use_stream=USE_STREAM)
        else:
            print("📝 Generating multiple test cases in BATCH mode...\n")
            all_outputs = [generate_batched_test_cases(requirement, version, use_stream=USE_STREAM)]

        end_time = time.time()  # ✅ end timer
        response_time_seconds = round(end_time - start_time, 2)

        # Parse outputs
        structured_all_cases = []
        for output_text in all_outputs:
            try:
                structured_cases = json.loads(output_text)
                if isinstance(structured_cases, dict):
                    structured_cases = [structured_cases]
            except json.JSONDecodeError:
                structured_cases = extract_structured_test_case(output_text)
            structured_all_cases.extend(structured_cases or [{"raw_output": output_text}])

        # ====== Stop monitoring after generation ======
        stop_event.set()
        monitor_thread.join()

        # Save JSON with system stats included
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename_json = os.path.join(
            OUTPUT_DIR, f"testcase_{version}_{mode}_{timestamp_str}.json"
        )
        with open(filename_json, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "version": version,
                "mode": mode,
                "requirement": requirement,
                "response_time_seconds": response_time_seconds,
                "generated_output": all_outputs,
                "structured_test_cases": structured_all_cases,
                "system_stats": stats_list
            }, f, indent=2, ensure_ascii=False)

        # Save Markdown
        filename_md = filename_json.replace(".json", ".md")
        with open(filename_md, "w", encoding="utf-8") as f:
            f.write("# 🧪 Generated Test Cases\n\n")
            f.write(f"**Requirement:** {json.dumps(requirement, indent=2)}\n\n")  # ✅ better formatting
            f.write(f"**Version:** {version}\n\n")
            f.write(f"**Mode:** {mode}\n\n")
            f.write(f"**Response Time (s):** {response_time_seconds}\n\n")
            f.write("---\n\n")
            for idx, case in enumerate(structured_all_cases, start=1):
                f.write(f"## Test Case {idx}\n\n")
                for key, value in case.items():
                    section_title = key.replace("_", " ").title()
                    f.write(f"### {section_title}\n")
                    if isinstance(value, list):
                        for item in value:
                            f.write(f"- {item}\n")
                    else:
                        f.write(f"{value}\n")
                    f.write("\n")
                f.write("---\n\n")

        print(f"✅ Test cases + system stats saved to {filename_json}")
        print(f"🗒️ Markdown version saved to {filename_md}")
        print(f"⏱️ Response time: {response_time_seconds} seconds")

    except Exception as e:
        stop_event.set()
        monitor_thread.join()
        print(f"❌ Error generating test cases: {e}")
