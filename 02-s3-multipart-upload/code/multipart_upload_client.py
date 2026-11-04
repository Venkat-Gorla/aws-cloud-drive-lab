"""
uv run code/multipart_upload_client.py
"""

from pathlib import Path
import json
from multipart_upload_handler import handler

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


def get_upload_event(number_of_parts, upload_id):
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


def validate_response(response):
    status_code = response["statusCode"]

    if status_code != 200:
        raise RuntimeError(
            f"Upload initialization failed. HTTP {status_code}: {response['body']}"
        )

    return json.loads(response["body"])


def main():
    _, number_of_parts = inspect_file(FILE_PATH)
    upload_id = get_upload_id()
    upload_event = get_upload_event(number_of_parts, upload_id)

    response = handler(upload_event, None)
    validate_response(response)


if __name__ == "__main__":
    main()
