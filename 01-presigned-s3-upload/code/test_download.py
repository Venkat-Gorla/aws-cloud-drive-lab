"""
uv run code/test_download.py
"""

import json
import boto3
import requests
from s3_download import generate_download_url

BUCKET_NAME = "aws-cloud-drive-vg"
KEY = "uploads/user-123/sample.json"

s3 = boto3.client("s3")


def main():
    download_url = generate_download_url(
        s3_client=s3,
        bucket=BUCKET_NAME,
        key=KEY,
    )

    response = requests.get(download_url, timeout=30)

    print(f"\nHTTP Status : {response.status_code}")
    response.raise_for_status()

    # Verify downloaded content
    downloaded_data = response.json()

    print("\nDownloaded Content:")
    print(json.dumps(downloaded_data, indent=2))

    print("\nDownload successful!")


if __name__ == "__main__":
    main()
