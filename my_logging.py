from loguru import logger
import sys
import os
from configs import cnf


def setup_logging():
    logger.remove()
    # adds logging to stderr
    if cnf.LOG_LEVEL == "DEBUG":
        log_format = (
            "<white>{time: YYYY-MM-DD HH:mm:ss.SSS} | </white>"
            "<lvl>[{level: <8}] "
            "</lvl><yellow>{name}  {function}:{line}</yellow> - "
            "<lvl>{message}</lvl>"
        )
        logger.configure(extra={"classname": "None"})
        logger.add(sys.stderr, format=log_format, level=cnf.LOG_LEVEL, colorize=True)
    else:
        log_format = "{time: YYYY-MM-DD HH:mm:ss} | [{level: <8}] | {message}"
        logger.add(sys.stderr, format=log_format, level=cnf.LOG_LEVEL)

    # TODO: Setup a separate logging format if not in debug.  get rid of classes and line numbers...

    # ! don't log to file on production.  run in docker so it should handle the log cleanup
    if cnf.LOG_LEVEL == "DEBUG" and not cnf.ENV_STATE == "prod":
        log_path = "./logs/"
        log_file = "harrymack.log"
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        logger.add(
            os.path.join(log_path, log_file),
            format=log_format,
            level="DEBUG",
            backtrace=True,
            diagnose=True,
        )

    return logger
