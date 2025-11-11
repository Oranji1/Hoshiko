import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from discord.utils import stream_supports_colour

LOG_DIR = Path("./logs/")
LOG_DIR.mkdir(exist_ok=True)

LEVEL_COLORS = [
    (logging.DEBUG, "\x1b[32;1m"),
    (logging.INFO, "\x1b[37;1m"),
    (logging.WARNING, "\x1b[33;1m"),
    (logging.ERROR, "\x1b[31;1m"),
    (logging.CRITICAL, "\x1b[41;1m"),
]

FORMATS = {
    level: logging.Formatter(
        f"\x1b[34;1m[%(asctime)s]\x1b[0m {color}[%(levelname)-8s]\x1b[0m "
        "\x1b[36;1m%(name)s\x1b[0m %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    for level, color in LEVEL_COLORS
}


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # noqa: PLR6301
        formatter = FORMATS.get(record.levelno)
        if formatter is None:
            formatter = FORMATS[logging.DEBUG]

        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        output = formatter.format(record)

        record.exc_text = None
        return output


def setup_logger(
    level: int | None = logging.INFO, max_mib: int = 32, backup_count: int = 5
) -> None:
    logger = logging.getLogger()
    logger.setLevel(level)

    fmt = logging.Formatter(
        "[%(asctime)s] [%(levelname)-8s] %(name)s: %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    supports_color = stream_supports_colour(console_handler.stream)
    console_handler.setFormatter(ColorFormatter() if supports_color else fmt)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        LOG_DIR / "hoshiko.log",
        maxBytes=max_mib * 1024 * 1024,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)
