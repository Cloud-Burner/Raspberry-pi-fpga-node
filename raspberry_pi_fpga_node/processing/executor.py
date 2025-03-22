from concurrent.futures import ThreadPoolExecutor

from loguru import logger

from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.external_interaction.s3 import upload_bytes
from raspberry_pi_fpga_node.processing.flash import Flash
from raspberry_pi_fpga_node.processing.lite_lang import LiteLangExecutor
from raspberry_pi_fpga_node.processing.video_write import VideoWriter

executor = ThreadPoolExecutor(max_workers=settings.max_threads)

camera = VideoWriter()
flasher = Flash()


async def fpga_process(instruction: bytes, flash_file: bytes, name: str):
    flasher.flash_fpga(flash_file=flash_file)

    video = camera.get_video(
        command_processor=LiteLangExecutor(instruction=instruction),
        position=settings.fpga_camera_position,
    )

    link = await upload_bytes(
        bucket=settings.result_bucket,
        file=video,
        name=name + f".{settings.video_format}",
    )
    logger.info(f"{link} uploaded")
    # todo publish link
