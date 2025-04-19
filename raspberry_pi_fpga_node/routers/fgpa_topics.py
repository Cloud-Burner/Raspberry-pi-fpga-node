"""This module contains the routing logic for fpga topics."""

import asyncio

from faststream.rabbit import RabbitQueue, RabbitRouter

from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.external_interaction.schemas import FpgaTask
from raspberry_pi_fpga_node.processing.fpga.executor import executor, fpga_process

green_board_queue = RabbitQueue(settings.green_board_q, durable=True)
router = RabbitRouter()


@router.subscriber(queue=green_board_queue)
async def handle(task: FpgaTask) -> None:
    """
    Handle a message from green plate q
    :param task:
    :return:
    """
    executor.submit(
        asyncio.run,
        fpga_process(user_id=task.user_id, number=task.number, task=task),
    )
