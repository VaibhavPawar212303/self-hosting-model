import os
from docx import Document

def convert_docx_to_txt(input_path, output_path=None):
    """
    Convert a DOCX file to a plain TXT file.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"❌ File not found: {input_path}")

    doc = Document(input_path)
    text_content = [para.text for para in doc.paragraphs]
    full_text = "\n".join(text_content)

    # If output not specified, replace .docx with .txt
    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = base + ".txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"✅ Converted: {input_path} → {output_path}")
    return output_path


if __name__ == "__main__":
    # Example usage
    input_file = "clientA-data/raw/Login_TestCases.docx"
    output_file = "clientA-data/text/Login_TestCases.txt"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    convert_docx_to_txt(input_file, output_file)
