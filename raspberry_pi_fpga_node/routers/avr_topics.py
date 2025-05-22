"""This module contains the routing logic for fpga topics."""

import asyncio

from faststream.rabbit import RabbitQueue, RabbitRouter

from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.external_interaction.schemas import ArduinoTask
from raspberry_pi_fpga_node.processing.fpga.executor import (
    arduino_nano_process,
    avr_executor,
)

async_node_avr_q = RabbitQueue(settings.async_node_avr, durable=True)
async_router = RabbitRouter()


@async_router.subscriber(queue=async_node_avr_q)
async def async_handle(task: ArduinoTask) -> None:
    """
    Handle a message from green plate q
    :param task:
    :return:
    """
    avr_executor.submit(
        asyncio.run,
        arduino_nano_process(task=task),
    )
