import logging
import sys

LOG_FORMAT = "[%(asctime)s.%(msecs)d][%(levelname)s][%(processName)s][%(process)d][%(threadName)s][%(name)s][%(pathname)s:%(lineno)s - %(funcName)s()] %(message)s"

logger = logging.getLogger("dojosdk")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
