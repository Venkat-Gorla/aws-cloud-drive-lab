import json
import boto3

BUCKET_NAME = "aws-cloud-drive-vg"

s3 = boto3.client("s3")


def generate_upload_url(
    s3_client,
    bucket: str,
    key: str,
    content_type: str,
    expires_in: int = 300,
) -> str:
    return s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": bucket,
            "Key": key,
            "ContentType": content_type,
        },
        ExpiresIn=expires_in,
        HttpMethod="PUT",
    )


def handler(event, context):
    # Mock identity for this POC
    user_id = "user-123"

    body = json.loads(event.get("body") or "{}")

    filename = body["filename"]
    content_type = body["content_type"]

    if "/" in filename or filename in (".", ".."):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid filename"}),
        }

    object_key = f"uploads/{user_id}/{filename}"

    url = generate_upload_url(
        s3,
        bucket=BUCKET_NAME,
        key=object_key,
        content_type=content_type,
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "upload_url": url,
            "object_key": object_key,
        }),
    }
