#!/usr/bin/env python3
from pathlib import Path
import boto3
from botocore.client import Config
from botocore import UNSIGNED

class DeadlockS3Downloader:
    ENDPOINT = "https://s3-cache.deadlock-api.com"
    BUCKET = "db-snapshot"
    PREFIX = "public/"
    DEST_ROOT = Path("./raw")

    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=self.ENDPOINT,
            config=Config(signature_version=UNSIGNED),
        )

    def list_objects(self):
        token = None
        while True:
            kwargs = dict(Bucket=self.BUCKET, Prefix=self.PREFIX, MaxKeys=1000)
            if token:
                kwargs["ContinuationToken"] = token
            resp = self.client.list_objects_v2(**kwargs)
            for obj in resp.get("Contents", []):
                key = obj["Key"]
                if key.endswith("/") or not key.startswith(self.PREFIX):
                    continue
                relative = key[len(self.PREFIX):]
                if relative.startswith("match_metadata/match_info") and relative.endswith(".parquet"):
                    yield obj
            if not resp.get("IsTruncated"):
                break
            token = resp.get("NextContinuationToken")

    def download_one(self, obj):
        key = obj["Key"]
        relative = key[len(self.PREFIX):]
        local_path = self.DEST_ROOT / relative
        local_path.parent.mkdir(parents=True, exist_ok=True)
        self.client.download_file(self.BUCKET, key, str(local_path))
        print(f"Downloaded: {relative}")

    def download_all(self):
        for obj in self.list_objects():
            self.download_one(obj)

if __name__ == "__main__":
    DeadlockS3Downloader().download_all()
