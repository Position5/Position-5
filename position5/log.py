import sys
import logging


def setup_logging():
    file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
    file_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

    dpy_logger = logging.getLogger("discord")
    dpy_logger.setLevel(logging.INFO)
    dpy_logger.addHandler(file_handler)

    position5_logger = logging.getLogger("position5")
    position5_logger.setLevel(logging.DEBUG)
    position5_logger.addHandler(stdout_handler)
