import os

def split_requirements(input_file, output_dir):
    """
    Splits a test cases .txt file into individual requirement files.
    Each requirement/test case is assumed to be separated by a blank line or starts with a number.
    """

    # Make sure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    buffer = []
    req_count = 1

    for line in lines:
        # Start of a new requirement if line begins with a number + dot
        if line.strip().startswith(tuple(str(i) + "." for i in range(1, 100))) and buffer:
            # Save the previous buffer
            file_name = f"req-{req_count:03}.txt"
            with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as out:
                out.write("".join(buffer).strip())
            buffer = []
            req_count += 1

        buffer.append(line)

    # Save the last buffer
    if buffer:
        file_name = f"req-{req_count:03}.txt"
        with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as out:
            out.write("".join(buffer).strip())

    print(f"✅ Split into {req_count} requirement files in: {output_dir}")


if __name__ == "__main__":
    # Example usage
    input_file = "clientA-data/text/Login_TestCases.txt"
    output_dir = "clientA-data/text/requirements"
    split_requirements(input_file, output_dir)
