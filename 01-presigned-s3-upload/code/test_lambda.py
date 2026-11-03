"""
uv run code/test_lambda.py
"""

import json
from lambda_function import handler
from urllib.parse import urlparse, parse_qs


def print_signature_details(upload_url):
    params = parse_qs(urlparse(upload_url).query)

    print("\nSignature Details:")
    for key, value in params.items():
        if key != "X-Amz-Signature":
            print(f"  {key}: {value[0]}")

    signature = params.get("X-Amz-Signature", [None])[0]
    print(f"  X-Amz-Signature: {'Present' if signature else 'Missing'}")


def print_response(response):
    body = json.loads(response["body"])

    print(f"\nHTTP Status : {response['statusCode']}")
    print(f"Object Key  : {body['object_key']}")
    print(f"\nPre-Signed URL:\n{body['upload_url']}")

    print_signature_details(body["upload_url"])


def main():
    event = {
        "body": json.dumps({
            "filename": "sample.json",
            "content_type": "application/json",
        })
    }

    response = handler(event, None)
    print_response(response)


if __name__ == "__main__":
    main()
