from botocore.client import BaseClient
from botocore.exceptions import ClientError

from infrastructure.logger import get_logger
from infrastructure.environment import env


logger = get_logger(f"{__name__}.S3Repository")


class S3Repository:
    def __init__(self, s3_client: BaseClient):
        self.client: BaseClient = s3_client
        self.BUCKET_NAME = env.rustfs.bucket_name

    async def ensure_bucket(self) -> bool:
        """Создаёт бакет, если его нет. Возвращает True при создании."""
        try:
            self.client.head_bucket(Bucket=self.BUCKET_NAME)
            logger.debug(f"Bucket {self.BUCKET_NAME} already exists")
            return False
        except ClientError as e:
            if not self._is_missing_bucket(e):
                raise

        try:
            self.client.create_bucket(Bucket=self.BUCKET_NAME)
            logger.info(f"Bucket {self.BUCKET_NAME} created")
            return True
        except ClientError as e:
            if self._is_bucket_already_exists(e):
                logger.debug(f"Bucket {self.BUCKET_NAME} already created")
                return False
            raise

    async def upload(self, key: str, data: bytes) -> None:
        try:
            self.client.put_object(Bucket=self.BUCKET_NAME, Key=key, Body=data)
        except ClientError as e:
            if not self._is_missing_bucket(e):
                raise
            logger.warning(
                f"Bucket {self.BUCKET_NAME} is missing, creating and retrying"
            )
            await self.ensure_bucket()
            self.client.put_object(Bucket=self.BUCKET_NAME, Key=key, Body=data)

    async def delete(self, key: str) -> None:
        self.client.delete_object(Bucket=self.BUCKET_NAME, Key=key)

    async def get_url(self, key: str) -> str:
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.BUCKET_NAME, "Key": key},
        )

    async def get_file(self, file_key: str) -> bytes:
        response = self.client.get_object(
            Bucket=self.BUCKET_NAME,
            Key=file_key,
        )
        file_bytes = response["Body"].read()
        response["Body"].close()

        return file_bytes

    @staticmethod
    def _is_missing_bucket(error: ClientError) -> bool:
        code = str(error.response.get("Error", {}).get("Code", ""))
        status = error.response.get("ResponseMetadata", {}).get(
            "HTTPStatusCode"
        )
        return code in {"404", "NoSuchBucket"} or status == 404

    @staticmethod
    def _is_bucket_already_exists(error: ClientError) -> bool:
        code = str(error.response.get("Error", {}).get("Code", ""))
        return code in {
            "BucketAlreadyExists",
            "BucketAlreadyOwnedByYou",
        }
