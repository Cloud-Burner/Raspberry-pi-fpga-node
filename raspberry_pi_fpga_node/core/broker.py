"""This module contains the broker initialization."""

from faststream.rabbit import RabbitBroker

broker = RabbitBroker(
    url="amqp://user:password@localhost:5672/",
)
