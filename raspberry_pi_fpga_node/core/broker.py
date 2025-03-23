"""This module contains the broker initialization."""

from faststream.rabbit import RabbitBroker

from raspberry_pi_fpga_node.core.settings import settings

broker = RabbitBroker(
    url=f"amqp://user:password@{settings.rabbit_host}:{settings.rabbit_port}/",
)
