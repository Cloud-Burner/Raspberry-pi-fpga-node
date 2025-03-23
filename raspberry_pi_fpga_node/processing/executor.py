"""This module thread pool and thread tasks for handle task."""

import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import time

from faststream.rabbit import RabbitQueue
from loguru import logger

from raspberry_pi_fpga_node.core.broker import broker
from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.external_interaction.s3 import upload_bytes
from raspberry_pi_fpga_node.external_interaction.schemas import ResultFpgaTask
from raspberry_pi_fpga_node.processing.flash import Flash
from raspberry_pi_fpga_node.processing.lite_lang import LiteLangExecutor
from raspberry_pi_fpga_node.processing.video_write import VideoWriter

result_exchange = RabbitQueue(name=settings.result_exc)

executor = ThreadPoolExecutor(max_workers=settings.max_threads)
camera = VideoWriter()
flasher = Flash()


async def fpga_process(
    instruction: bytes, flash_file: bytes, username: str, number: str
) -> None:
    """Make all task processes asynchronously in parallel thread.
    :param instruction:
    :param flash_file:
    :param username:
    :param number: number of the task
    """
    name = username + "-" + number + "-" + str(time()).replace(".", "-")
    with tempfile.NamedTemporaryFile(
        delete=True, suffix=".svf", dir=Path(settings.dynamic_dir)
    ) as temp_file:
        temp_file.write(flash_file)
        temp_file.flush()
        flasher.flash_fpga(flash_file_path=temp_file.name)
        video = camera.get_video(
            command_processor=LiteLangExecutor(instruction=instruction),
            position=settings.fpga_camera_position,
        )
        link = await upload_bytes(
            bucket=settings.result_bucket,
            file=video,
            name=name + f".{settings.video_format}",
        )
        logger.info(f"Vido uploaded, download on {link}")
        logger.info(f"Tempfile {temp_file.name} deleted")
        await broker.publish(
            message=ResultFpgaTask(username=username, number=number, link=link),
            queue=result_exchange,
        )
