# ai/config.py
# Logging configurations.

import logging.config
import sys
from pathlib import Path

from rich.logging import RichHandler

# Directories
BASE_DIR = Path(__file__).parent.parent.absolute()
LOGS_DIR = Path(BASE_DIR, "logs")

# Create a new directory if doesn't exist
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Logger
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "minimal": {"format": "%(message)s"},
        "detailed": {
            "format": "%(levelname)s %(asctime)s\
                       [%(filename)s:%(funcName)s:%(lineno)d]\n%(message)s\n"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "minimal",
            "level": logging.DEBUG,
        },
        "info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "info.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.INFO,
        },
        "error": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "error.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.ERROR,
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console", "info", "error"],
            "level": logging.INFO,
            "propagate": True,
        },
    },
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger("root")
logger.handlers[0] = RichHandler(markup=True)

# Add success level between WARNING and INFO
logging.SUCCESS = 25
logging.addLevelName(logging.SUCCESS, "SUCCESS")
setattr(logger, "success", lambda message, *args: logger._log(logging.SUCCESS, message, args))

# if __name__ == '__main__':
#     # Sample messages (not we use configured `logger` now)
#     logger.debug("Used for debugging your code.")
#     logger.info("Informative messages from your code.")
#     logger.success('success')
#     logger.warning("Everything works but there is something to be aware of.")
#     logger.error("There's been a mistake with the process.")
#     logger.critical("There is something terribly wrong and process may terminate.")
