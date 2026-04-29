import logging
import os
from logging.handlers import TimedRotatingFileHandler


def configure_logger():
    """
    Configure the application logger.

    Sets up both console and file logging handlers.
    Console output is set to INFO level, while file logging captures DEBUG and above.

    Log files are stored in ~/.local/var/log/train-board/ and rotate daily at midnight.

    Returns:
        logging.Logger: Configured logger instance for the application
    """
    logger = logging.getLogger("station_board")

    # Prevent adding multiple handlers if logger is configured multiple times
    if logger.handlers:
        return logger

    # Set the root logger level
    logger.setLevel(logging.DEBUG)

    # Create console handler with INFO level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create timed rotating file handler
    # Logs to ~/.local/var/log/train-board/ following XDG Base Directory spec
    log_dir = os.path.expanduser("~/.local/var/log/train-board")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "train-board.log")
    # TimedRotatingFileHandler rotates at midnight, keeps 30 days of logs
    file_handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=30, utc=False
    )
    file_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
