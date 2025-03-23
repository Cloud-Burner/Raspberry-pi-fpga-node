"""This module contains the routing logic for fpga topics."""

import asyncio

from faststream.rabbit import RabbitQueue, RabbitRouter
from loguru import logger

from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.external_interaction.s3 import download
from raspberry_pi_fpga_node.external_interaction.schemas import FpgaTask
from raspberry_pi_fpga_node.processing.executor import executor, fpga_process

green_board_queue = RabbitQueue(settings.green_board_q, durable=True)
router = RabbitRouter()


@router.subscriber(queue=green_board_queue)
async def handle(task: FpgaTask) -> None:
    """
    Handle a message from green plate q
    :param task:
    :return:
    """

    instruction = await download(
        bucket=settings.task_bucket, file=task.instruction_file
    )
    logger.info(instruction)
    flash_file = await download(bucket=settings.task_bucket, file=task.flash_file)
    executor.submit(
        asyncio.run,
        fpga_process(
            instruction=instruction,
            flash_file=flash_file,
            username=task.username,
            number=task.number,
        ),
    )
