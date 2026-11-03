"""
uv run code/test_lambda.py
"""

import json
from lambda_function import handler
from urllib.parse import urlparse, parse_qs

event = {
    "body": json.dumps({
        "filename": "sample.json",
        "content_type": "application/json",
    })
}


def print_signature_details(upload_url):
    params = parse_qs(urlparse(upload_url).query)

    print("\nSignature Details:")
    for key, value in params.items():
        if key != "X-Amz-Signature":
            print(f"  {key}: {value[0]}")


def print_response(response):
    body = json.loads(response["body"])

    print(f"\nHTTP Status : {response['statusCode']}")
    print(f"Object Key  : {body['object_key']}")
    print(f"\nPre-Signed URL:\n{body['upload_url']}\n")

    print_signature_details(body["upload_url"])


def main():
    response = handler(event, None)
    print_response(response)


if __name__ == "__main__":
    main()
