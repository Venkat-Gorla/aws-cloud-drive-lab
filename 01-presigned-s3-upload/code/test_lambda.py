"""
uv run code/test_lambda.py
"""

import json
from lambda_function import handler

event = {
    "body": json.dumps({
        "filename": "sample.pdf",
        "content_type": "application/pdf",
    })
}


def print_response(response):
    body = json.loads(response["body"])

    print(f"\nHTTP Status : {response['statusCode']}")
    print(f"Object Key  : {body['object_key']}")
    print(f"\nPre-Signed URL:\n{body['upload_url']}\n")


def main():
    response = handler(event, None)
    print_response(response)


if __name__ == "__main__":
    main()
