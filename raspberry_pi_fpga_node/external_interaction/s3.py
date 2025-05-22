"""This module contains the s3 functionality."""

from typing import Any
from urllib.parse import urlparse, urlunparse

import aiofiles
from aiobotocore.session import get_session
from pydantic import AnyUrl

from raspberry_pi_fpga_node.core.settings import settings


def rewrite_url(url: str) -> str:
    parsed = urlparse(url)

    new_path = f"/s3{parsed.path}"

    return urlunparse(("", "", new_path, "", parsed.query, ""))


session = get_session()


creds = {
    "service_name": "s3",
    "endpoint_url": settings.s3_url,
    "aws_access_key_id": settings.access_key,
    "aws_secret_access_key": settings.secret_key,
}


async def upload_bytes(bucket: str, file: bytes, name: str) -> str:
    """Загружает файл из байтов (оперативы)"""
    async with session.create_client(**creds) as s3_client:
        await s3_client.put_object(Bucket=bucket, Key=name, Body=file)
        return rewrite_url(
            await s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": name},
                ExpiresIn=360000,
            )
        )


async def upload_from_disk(bucket: str, file_path: str) -> AnyUrl:
    """Загружает файл с диска"""
    async with session.create_client(**creds) as s3_client:
        async with aiofiles.open(file_path, "rb") as file:
            data = await file.read()
            await s3_client.put_object(
                Bucket=bucket, Key=file_path.split("/")[-1], Body=data
            )
            return AnyUrl(
                await s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": bucket, "Key": file_path.split("/")[-1]},
                    ExpiresIn=360000,
                )
            )


async def download(bucket: str, file: str) -> bytes | Any:
    """Скачивает файл, в оперативу
    :param bucket:
    :param file:
    """
    async with session.create_client(**creds) as s3_client:
        response = await s3_client.get_object(Bucket=bucket, Key=file)
        return await response["Body"].read()
