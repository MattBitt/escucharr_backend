from loguru import logger
import sys
import os

# need to pull from enviornment
config = {"log_level": "DEBUG", "enviornment": "env_dev"}


def setup_logging():
    # logger.remove(0)
    # adds logging to stderr
    if config["log_level"] == "DEBUG":
        log_format = (
            "<white>{time: YYYY-MM-DD HH:mm:ss.SSS} | </white>"
            "<lvl>[{level: <8}]"
            "</lvl><yellow>{name}:<c>{extra[classname]}</c>:{function}:{line}</yellow> - "
            "<lvl>{message}</lvl>"
        )
        logger.configure(extra={"classname": "None"})
        logger.add(
            sys.stderr, format=log_format, level=config["log_level"], colorize=True
        )
    else:
        log_format = "{time: YYYY-MM-DD HH:mm:ss} | [{level: <8}] | {message}"
        logger.add(sys.stderr, format=log_format, level=config["log_level"])

    # TODO: Setup a separate logging format if not in debug.  get rid of classes and line numbers...

    # ! don't log to file on production.  run in docker so it should handle the log cleanup
    if config["log_level"] == "DEBUG" and not config["enviornment"] == "env_prod":
        log_path = "./logs/"
        log_file = "harrymack.log"
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        logger.add(
            os.path.join(log_path, log_file),
            format=log_format,
            level=config["log_level"],
            backtrace=True,
            diagnose=True,
        )

    return logger
