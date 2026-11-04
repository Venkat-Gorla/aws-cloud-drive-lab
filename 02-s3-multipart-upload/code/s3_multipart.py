def initiate_multipart_upload(
    s3_client,
    bucket: str,
    key: str,
    content_type: str
) -> str:
    response = s3_client.create_multipart_upload(
        Bucket=bucket,
        Key=key,
        ContentType=content_type,
    )
    return response["UploadId"]


def generate_presigned_part_url(
    s3_client,
    bucket: str,
    key: str,
    upload_id: str,
    part_number: int,
    expires_in: int = 600,
) -> str:
    return s3_client.generate_presigned_url(
        ClientMethod="upload_part",
        Params={
            "Bucket": bucket,
            "Key": key,
            "UploadId": upload_id,
            "PartNumber": part_number,
        },
        ExpiresIn=expires_in,
        HttpMethod="PUT",
    )


def complete_multipart_upload(s3_client, bucket, key, upload_id, parts):
    return s3_client.complete_multipart_upload(
        Bucket=bucket,
        Key=key,
        UploadId=upload_id,
        MultipartUpload={"Parts": parts},
    )
