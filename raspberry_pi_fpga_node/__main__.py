"""This module contains the startup server."""

import uvicorn
from faststream.asgi import AsgiFastStream
from loguru import logger
from uvicorn import Server

from raspberry_pi_fpga_node.core.broker import broker
from raspberry_pi_fpga_node.core.logger import setup_logger
from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.routers.fgpa_topics import router

broker.include_router(router)

setup_logger(settings.log_level)
app = AsgiFastStream(broker, logger=logger)


def main() -> None:
    """
    run the app
    :return:
    """
    config = uvicorn.Config(app="__main__:app", log_config=None)
    server = Server(config=config)
    server.run()


if __name__ == "__main__":
    main()
