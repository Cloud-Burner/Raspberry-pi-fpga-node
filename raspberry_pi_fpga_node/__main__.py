"""This module contains the startup server."""

import uvicorn
from faststream.asgi import AsgiFastStream
from loguru import logger
from uvicorn import Server

from raspberry_pi_fpga_node.core.broker import broker
from raspberry_pi_fpga_node.core.logger import log_setup
from raspberry_pi_fpga_node.core.settings import settings
from raspberry_pi_fpga_node.routers.fgpa_topics import async_router, sync_router

if settings.MODE == "async":
    logger.info("Starting async mode")
    broker.include_router(async_router)
else:
    logger.info("Starting sync mode")
    broker.include_router(sync_router)

log_setup()
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
