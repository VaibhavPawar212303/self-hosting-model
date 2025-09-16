import os

def normalize_requirement(content: str, req_id: str) -> str:
    """
    Normalize raw requirement text into a structured format.
    """
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    title = lines[0] if lines else f"Requirement {req_id}"

    # Default placeholders
    steps = []
    expected = "Expected result not specified."

    for line in lines[1:]:
        if "expected" in line.lower():
            expected = line.split(":", 1)[-1].strip()
        else:
            steps.append(line)

    # Format into structured requirement
    normalized = [
        f"ID: {req_id}",
        f"Title: {title}",
        "Steps:"
    ]

    for i, step in enumerate(steps, start=1):
        normalized.append(f"  {i}. {step}")

    normalized.append(f"Expected Result: {expected}")
    return "\n".join(normalized)


def normalize_all(input_dir: str, output_dir: str):
    """
    Normalize all req-xxx.txt files in a folder into structured format.
    """
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.startswith("req-") and file_name.endswith(".txt"):
            req_id = file_name.replace(".txt", "").upper()
            with open(os.path.join(input_dir, file_name), "r", encoding="utf-8") as f:
                content = f.read()

            normalized_text = normalize_requirement(content, req_id)

            output_path = os.path.join(output_dir, file_name)
            with open(output_path, "w", encoding="utf-8") as out:
                out.write(normalized_text)

            print(f"✅ Normalized: {file_name} → {output_path}")

    print(f"\nAll requirements normalized and saved in {output_dir}")


if __name__ == "__main__":
    input_dir = "clientA-data/text/requirements"
    output_dir = "clientA-data/text/normalized"
    normalize_all(input_dir, output_dir)
