import os, boto3

S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://minio:9000")
S3_BUCKET = os.getenv("S3_BUCKET", "hypernode-checkpoints")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "minioadmin")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "minioadmin")
S3_USE_SSL = os.getenv("S3_USE_SSL", "false").lower() == "true"

def s3():
    return boto3.resource(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        use_ssl=S3_USE_SSL,
    )

def upload(local_path: str, key: str):
    s3().Bucket(S3_BUCKET).upload_file(local_path, key)
    return f"s3://{S3_BUCKET}/{key}"
