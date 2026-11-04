"""
uv run code/multipart_upload_client.py
"""

from pathlib import Path
import json
from multipart_upload_handler import handler
import requests
from upload_completion_handler import handler as upload_completion_handler

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


def get_initiation_event(number_of_parts, upload_id):
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


def upload_file_parts(file_path, part_urls):
    uploaded_parts = []

    with file_path.open("rb") as file:
        for part in part_urls:
            part_data = file.read(PART_SIZE)

            response = requests.put(
                part["upload_url"],
                data=part_data,
            )
            response.raise_for_status()

            uploaded_parts.append({
                "PartNumber": part["part_number"],
                "ETag": response.headers["ETag"],
            })

    return uploaded_parts


def get_completion_event(upload_id, parts):
    return {
        "body": json.dumps({
            "filename": FILE_PATH.name,
            "upload_id": upload_id,
            "parts": parts,
        })
    }


def main():
    _, number_of_parts = inspect_file(FILE_PATH)
    upload_id = get_upload_id()
    initiation_event = get_initiation_event(number_of_parts, upload_id)

    initiation_response = handler(initiation_event, None)

    initiation_body = validate_response(initiation_response)
    part_urls = initiation_body["part_urls"]
    uploaded_parts = upload_file_parts(FILE_PATH, part_urls)

    print(f"\nSuccessfully uploaded {len(uploaded_parts)} parts to S3.")

    completion_event = get_completion_event(
        initiation_body["upload_id"],
        uploaded_parts,
    )

    completion_response = upload_completion_handler(completion_event, None)
    completion_body = validate_response(completion_response)

    print("\nMultipart upload completed successfully.")


if __name__ == "__main__":
    main()
