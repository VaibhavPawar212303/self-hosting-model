import os
import requests
import json
import time
from openpyxl import Workbook

# =====================
# CONFIG
# =====================
MODEL_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b-instruct-q4_K_M"
MAX_RETRIES = 3
TIMEOUT = 60  # seconds


def ask_model(prompt: str) -> str:
    """
    Send prompt to self-hosted LLaMA (Ollama) and return the generated text.
    Supports streaming JSON responses, retries, and timeouts.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": 500,
        "temperature": 0.3
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"\n🚀 Sending prompt to model (attempt {attempt})...")
            resp = requests.post(MODEL_ENDPOINT, json=payload, stream=True, timeout=TIMEOUT)
            resp.raise_for_status()

            output_text = ""
            for line in resp.iter_lines():
                if not line:
                    continue
                try:
                    obj = json.loads(line.decode("utf-8"))
                    if "response" in obj:
                        chunk = obj["response"]
                        output_text += chunk
                        # 🔎 Debug: show each chunk as it arrives
                        print(f"[STREAM] {chunk}", end="", flush=True)
                    if obj.get("done", False):
                        break
                except json.JSONDecodeError:
                    print("⚠️ Skipped malformed chunk")
                    continue

            print("\n\n==== Final Combined Output ====")
            print(output_text.strip())
            print("================================\n")

            return output_text.strip()

        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            if attempt < MAX_RETRIES:
                wait_time = 2 ** attempt
                print(f"⏳ Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise RuntimeError(f"❌ Model request failed after {MAX_RETRIES} attempts: {e}")


def generate_manual_testcases(req_dir: str, output_file: str):
    """
    Generate manual test cases from requirement files in `req_dir` and save to Excel.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "TestCases"

    headers = [
        "Test Case ID", "Requirement ID", "Title",
        "Pre-Conditions", "Test Steps", "Test Data",
        "Expected Result", "Actual Result", "Status", "Remarks"
    ]
    ws.append(headers)

    req_files = sorted([f for f in os.listdir(req_dir) if f.endswith(".txt")])
    tc_count = 1

    for req_file in req_files:
        with open(os.path.join(req_dir, req_file), "r", encoding="utf-8") as f:
            req_text = f.read()

        # Prompt to model
        prompt = f"""
You are a QA engineer. Convert this requirement into a manual test case.
Requirement:
{req_text}

Output format (strict):
Title:
Pre-Conditions:
Test Steps:
Test Data:
Expected Result:
"""
        generated = ask_model(prompt)

        # Parse model output into fields
        title, pre, steps, data, expected = "", "", "", "", ""
        for line in generated.splitlines():
            line = line.strip()
            if line.startswith("Title:"):
                title = line.replace("Title:", "").strip()
            elif line.startswith("Pre-Conditions:"):
                pre = line.replace("Pre-Conditions:", "").strip()
            elif line.startswith("Test Steps:"):
                steps = line.replace("Test Steps:", "").strip()
            elif line.startswith("Test Data:"):
                data = line.replace("Test Data:", "").strip()
            elif line.startswith("Expected Result:"):
                expected = line.replace("Expected Result:", "").strip()

        ws.append([
            f"TC-{tc_count:03}",
            req_file.replace(".txt", ""),
            title,
            pre,
            steps,
            data,
            expected,
            "", "", ""  # Actual Result, Status, Remarks left blank
        ])
        tc_count += 1

    wb.save(output_file)
    print(f"✅ Manual test cases saved to {output_file}")


if __name__ == "__main__":
    req_dir = "clientA-data/text/normalized"
    output_file = "clientA-data/train/Manual_TestCases.xlsx"
    generate_manual_testcases(req_dir, output_file)
