import json
import boto3

from s3_multipart import (
    initiate_multipart_upload,
    generate_presigned_part_url,
)

BUCKET_NAME = "aws-cloud-drive-vg"

s3 = boto3.client("s3")


def get_part_urls(object_key, upload_id, number_of_parts):
    part_urls = []

    for part_number in range(1, number_of_parts + 1):
        url = generate_presigned_part_url(
            s3_client=s3,
            bucket=BUCKET_NAME,
            key=object_key,
            upload_id=upload_id,
            part_number=part_number,
        )

        part_urls.append({
            "part_number": part_number,
            "upload_url": url,
        })

    return part_urls


def handler(event, context):
    user_id = "user-123"
    body = json.loads(event.get("body") or "{}")

    filename = body["filename"]
    content_type = body["content_type"]
    number_of_parts = body["number_of_parts"]

    object_key = f"lab-02-multipart/{user_id}/{filename}"

    upload_id = body.get("upload_id")

    if not upload_id:
        upload_id = initiate_multipart_upload(
            s3_client=s3,
            bucket=BUCKET_NAME,
            key=object_key,
            content_type=content_type,
        )

    part_urls = get_part_urls(object_key, upload_id, number_of_parts)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "upload_id": upload_id,
            "object_key": object_key,
            "part_urls": part_urls,
        }),
    }
