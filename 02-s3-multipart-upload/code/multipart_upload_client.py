"""
uv run code/multipart_upload_client.py
"""

from pathlib import Path
import json

FILE_PATH = Path("code/fixtures/sample-document.pdf")
PART_SIZE = 5 * 1024 * 1024  # 5 MiB


def inspect_file(file_path: Path):
    file_size = file_path.stat().st_size
    number_of_parts = (file_size + PART_SIZE - 1) // PART_SIZE

    print(f"File: {file_path.name} ({file_size / (1024 * 1024):.2f} MiB)")
    print(f"Parts: {number_of_parts}")

    return file_size, number_of_parts


def get_upload_id():
    upload_id = input(
        "Enter existing UploadId (press Enter for new upload): ").strip()
    return upload_id or None


def get_upload_event(number_of_parts, upload_id=None):
    body = {
        "filename": FILE_PATH.name,
        "content_type": "application/pdf",
        "number_of_parts": number_of_parts,
    }

    if upload_id:
        body["upload_id"] = upload_id

    return {
        "body": json.dumps(body)
    }


def main():
    _, number_of_parts = inspect_file(FILE_PATH)
    upload_id = get_upload_id()


if __name__ == "__main__":
    main()
