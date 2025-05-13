from loguru import logger
from faststream.rabbit import RabbitQueue, RabbitRouter, RabbitMessage
from raspberry_pi_fpga_node.core.broker import broker
from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.external_interaction.schemas import (
    FpgaTask,
    ResultFpgaTask,
)
from raspberry_pi_fpga_node.processing.fpga.executor import result_queue


def error_async_fpga_handler(func):
    async def wrapper(task: FpgaTask, msg: RabbitMessage):
        try:
            await func(msg)
        except Exception as exc:
            logger.error(f"Error in task {func.__name__}: {exc}")

            await broker.publish(
            ResultFpgaTask(
                    user_id=task.user_id,
                    number=task.number,
                    link=f"{settings.origin}/error",
                ),
                queue=result_queue,
            )

    return wrapper
