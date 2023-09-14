import logging

from rich.logging import RichHandler

logger = logging.getLogger(__name__)

# Handler to determine where logs go: stdout or file
shell_handler = RichHandler()
file_handler = logging.FileHandler("sus.log")

# logger.setLevel(logging.WARNING)
# shell_handler.setLevel(logging.WARNING)
# file_handler.setLevel(logging.WARNING)

fmt = logging.Formatter("[%(filename)s:%(lineno)d] %(levelname)s %(message)s")
shell_handler.setFormatter(fmt)
file_handler.setFormatter(fmt)

logger.addHandler(shell_handler)
logger.addHandler(file_handler)
