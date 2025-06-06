"""This module thread pool and thread tasks for handle task."""

import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import time

from faststream.rabbit import RabbitQueue
from loguru import logger

from raspberry_pi_fpga_node.core.broker import broker
from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.external_interaction.s3 import download, upload_bytes
from raspberry_pi_fpga_node.external_interaction.schemas import (
    ArduinoTask,
    FpgaSyncTask,
    FpgaTask,
    ResultArduinoTask,
    ResultFpgaTask,
)
from raspberry_pi_fpga_node.processing.fpga.flash import Flash
from raspberry_pi_fpga_node.processing.fpga.lite_lang import LiteLangExecutor
from raspberry_pi_fpga_node.processing.fpga.video_write import VideoWriter

result_queue = RabbitQueue(name=settings.result_queue)

fpga_executor = ThreadPoolExecutor(max_workers=settings.max_threads)
avr_executor = ThreadPoolExecutor(max_workers=settings.max_threads)
camera = VideoWriter() if settings.MODE == "async" else None
flasher = Flash()
fpga_lock = threading.Lock()
avr_lock = threading.Lock()


async def fpga_process(task: FpgaTask) -> None:
    """Make all task processes asynchronously in parallel thread."""
    with fpga_lock:
        instruction = await download(
            bucket=settings.task_bucket, file=task.instruction_file
        )
        logger.info(instruction)
        flash_file = await download(bucket=settings.task_bucket, file=task.flash_file)

        name = (
            str(task.user_id) + "-" + task.number + "-" + str(time()).replace(".", "-")
        )

        with tempfile.NamedTemporaryFile(
            delete=True, suffix=".svf", dir=Path(settings.dynamic_dir)
        ) as temp_file:
            temp_file.write(flash_file)
            temp_file.flush()
            flasher.flash_fpga(flash_file_path=temp_file.name)
            video = camera.get_video(
                command_processor=LiteLangExecutor(
                    instruction=instruction, pins=settings.fpga_pins
                ),
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
            message=ResultFpgaTask(
                user_id=task.user_id, number=task.number, link=str(link)
            ),
            queue=result_queue,
        )
        logger.info(f"Result sent to user:{task.user_id}")


async def arduino_nano_process(task: ArduinoTask) -> None:
    """Make all task processes asynchronously in parallel thread."""
    with avr_lock:
        instruction = await download(
            bucket=settings.task_bucket, file=task.instruction_file
        )
        logger.info(instruction)
        flash_file = await download(bucket=settings.task_bucket, file=task.flash_file)

        name = (
            str(task.user_id) + "-" + task.number + "-" + str(time()).replace(".", "-")
        )

        with tempfile.NamedTemporaryFile(
            delete=True, suffix=".hex", dir=Path(settings.dynamic_dir)
        ) as temp_file:
            temp_file.write(flash_file)
            temp_file.flush()
            logger.info("Start flash")
            flasher.flash_arduino_nano(flash_file_path=temp_file.name)
            logger.info("call get video")
            video = camera.get_video(
                command_processor=LiteLangExecutor(
                    instruction=instruction, pins=settings.arduino_pins
                ),
                position=settings.arduino_camera_position,
            )
            link = await upload_bytes(
                bucket=settings.result_bucket,
                file=video,
                name=name + f".{settings.video_format}",
            )
            logger.info(f"Vido uploaded, download on {link}")
            logger.info(f"Tempfile {temp_file.name} deleted")
        await broker.publish(
            message=ResultArduinoTask(
                user_id=task.user_id, number=task.number, link=str(link)
            ),
            queue=result_queue,
        )
        logger.info(f"Result sent to user:{task.user_id}")


async def sync_fpga_process(task: FpgaSyncTask) -> None:
    """Make all task processes synchronously in parallel thread."""
    if task.flash_file:
        logger.info("Starting download flash file")
        flash_file = await download(bucket=settings.task_bucket, file=task.flash_file)
        with tempfile.NamedTemporaryFile(
            delete=True, suffix=".svf", dir=Path(settings.dynamic_dir)
        ) as temp_file:
            temp_file.write(flash_file)
            temp_file.flush()
            flasher.flash_fpga(flash_file_path=temp_file.name)
            return
    if task.instruction:
        logger.info("Start instruction")
        command_processor = LiteLangExecutor(
            instruction=task.instruction.encode("utf-8")
        )
        for _ in range(31):
            command_processor.next()
        return
