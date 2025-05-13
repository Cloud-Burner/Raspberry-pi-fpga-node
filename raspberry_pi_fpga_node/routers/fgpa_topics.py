"""This module contains the routing logic for fpga topics."""

import asyncio

from faststream.rabbit import RabbitQueue, RabbitRouter, RabbitMessage

from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.external_interaction.schemas import FpgaSyncTask, FpgaTask
from raspberry_pi_fpga_node.middleware import error_async_fpga_handler
from raspberry_pi_fpga_node.processing.fpga.executor import (
    executor,
    fpga_process,
    sync_fpga_process,
)

async_node_q = RabbitQueue(settings.async_node_q, durable=True)
sync_node_q = RabbitQueue(settings.sync_node_q, durable=True)
async_router = RabbitRouter()
sync_router = RabbitRouter()


@async_router.subscriber(queue=async_node_q, no_ack=True)
@error_async_fpga_handler
async def async_handle(task: FpgaTask, msg: RabbitMessage) -> None:
    """
    Handle a message from green plate q
    :param task:
    :return:
    """
    await fpga_process(task=task)
    await msg.ack()


@sync_router.subscriber(queue=sync_node_q)
async def sync_handle(task: FpgaSyncTask) -> None:
    """
    Handle a message from green plate q
    :param task:
    :return:
    """
    executor.submit(
        asyncio.run,
        sync_fpga_process(task=task),
    )
