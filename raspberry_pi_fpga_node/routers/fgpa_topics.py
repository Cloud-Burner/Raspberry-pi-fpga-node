"""This module contains the routing logic for fpga topics."""

from faststream.rabbit import RabbitQueue, RabbitRouter

from raspberry_pi_fpga_node.core.settings import settings

green_board_queue = RabbitQueue(settings.green_board_q, durable=True)
router = RabbitRouter()


@router.subscriber(queue=green_board_queue)
async def handle(msg):
    """
    Handle a message from green plate q
    :param msg:
    :return:
    """
    print(msg)
