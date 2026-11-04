import json
import boto3
from s3_multipart import complete_multipart_upload

BUCKET_NAME = "aws-cloud-drive-vg"

s3 = boto3.client("s3")


def handler(event, context):
    user_id = "user-123"
    body = json.loads(event.get("body") or "{}")

    filename = body["filename"]
    upload_id = body["upload_id"]
    parts = body["parts"]

    object_key = f"lab-02-multipart/{user_id}/{filename}"

    result = complete_multipart_upload(
        s3_client=s3,
        bucket=BUCKET_NAME,
        key=object_key,
        upload_id=upload_id,
        parts=parts,
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Multipart upload completed successfully",
            "object_key": object_key,
            "etag": result["ETag"],
            "location": result.get("Location"),
        }),
    }
