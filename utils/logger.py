from loguru import logger
import sys
from pathlib import Path

# remove the default sink
logger.remove()

# create a folder for logs
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# general logs to the console
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
    level="INFO",
    enqueue=True
)

# UI‑logs
logger.add(
    log_dir / "ui_tests.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <6} | {name}:{function}: {line} | {message}",
    level="DEBUG",
    rotation="10 MB",
    compression="zip",
    enqueue=True,
    filter=lambda record: "ui" in record["extra"]
)

# API‑logs
logger.add(
    log_dir / "api_tests.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG",
    rotation="10 MB",
    compression="zip",
    enqueue=True,
    filter=lambda record: "api" in record["extra"]
)

# errors in file
logger.add(
    log_dir / "errors.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}: {line} - {message}",
    level="ERROR",
    rotation="5 MB",
    compression="zip",
)

# custom level STEP
logger.level("STEP", no=25, color="<cyan>", icon="🟦")

# related loggers
ui_logger = logger.bind(ui=True)
api_logger = logger.bind(api=True)
