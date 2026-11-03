def generate_download_url(
    s3_client,
    bucket: str,
    key: str,
    expires_in: int = 300,
) -> str:
    return s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket,
            "Key": key,
        },
        ExpiresIn=expires_in,
        HttpMethod="GET",
    )
