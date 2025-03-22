"""This module contains the startup server"""

import uvicorn
from faststream.asgi import AsgiFastStream
from loguru import logger
from uvicorn import Server

from raspberry_pi_fpga_node.core.broker import broker
from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.routers.fgpa_topics import router


def init() -> AsgiFastStream:
    """
    initialize the app
    :return: AsgiFastStream
    """
    broker.include_router(router)
    return AsgiFastStream(broker, logger=logger)


def main() -> None:
    """
    run the app
    :return:
    """
    config = uvicorn.Config(app="__main__:app", log_level=settings.log_level)
    server = Server(config=config)
    server.run()


if __name__ == "__main__":
    app = init()
    main()
