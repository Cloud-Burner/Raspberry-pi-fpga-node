import aiobotocore
from aiobotocore.session import get_session
from pydantic import AnyUrl

# Конфигурация MinIO (замени своими данными)
S3_ENDPOINT_URL = "http://localhost:9000"  # Адрес MinIO
ACCESS_KEY = "admin"
SECRET_KEY = "password123"
BUCKET_NAME = "mybucket"

# Создание сессии
session = get_session()

import aiofiles


class S3:
    def __init__(self):
        self.session = get_session()
        self.client = session.create_client(
                "s3",
                endpoint_url=S3_ENDPOINT_URL,
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,)
    async def upload_file(self, path: str, filename: str, bucket) -> AnyUrl:
        """Загружает файл"""
        async with aiofiles.open(path, "rb") as file:
            data = await file.read()
            await self.client.put_object(Bucket=bucket, Key=filename, Body=data)



async def download_file(object_name, save_path):
    """Асинхронно скачивает файл из MinIO"""
    async with session.create_client(
        "s3",
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    ) as s3_client:
        response = await s3_client.get_object(Bucket=BUCKET_NAME, Key=object_name)
        async with aiofiles.open(save_path, "wb") as f:
            await f.write(await response["Body"].read())  # Асинхронно записываем
        print(f"✅ Файл {object_name} скачан в {save_path}")

# Пример вызова
asyncio.run(download_file("uploaded_test.txt", "downloaded_test.txt"))


async def get_presigned_url(object_name, expiration=3600):
    """Создаёт асинхронную временную ссылку на скачивание файла"""
    async with session.create_client(
        "s3",
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    ) as s3_client:
        url = await s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": object_name},
            ExpiresIn=expiration,
        )
        return url

# Пример вызова
print(asyncio.run(get_presigned_url("uploaded_test.txt")))



async def delete_file(object_name):
    """Асинхронно удаляет файл из MinIO"""
    async with session.create_client(
        "s3",
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    ) as s3_client:
        await s3_client.delete_object(Bucket=BUCKET_NAME, Key=object_name)
        print(f"🗑 Файл {object_name} удалён из MinIO")

# Пример вызова
asyncio.run(delete_file("uploaded_test.txt"))