"""
uv run code/test_multipart_upload.py
"""

import json
from multipart_upload_handler import handler

event = {
    "body": json.dumps({
        "filename": "sample-document.pdf",
        "content_type": "application/pdf",
        "number_of_parts": 2,
    })
}


def print_response(response):
    body = json.loads(response["body"])

    print(f"\nHTTP Status : {response['statusCode']}")
    print(f"Object Key  : {body['object_key']}")
    print(f"Upload ID   : {body['upload_id']}")

    print("\nGenerated Part URLs:")

    for part in body["part_urls"]:
        print(f"  Part Number : {part['part_number']}")
        print("  Upload URL  : Generated successfully")


def main():
    response = handler(event, None)
    print_response(response)


if __name__ == "__main__":
    main()
