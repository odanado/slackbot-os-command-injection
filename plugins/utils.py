import logging
import os


def _mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def init_logger(name):
    logger = logging.getLogger(name)
    _mkdir('logs')
    fh = logging.FileHandler('logs/{}.log'.format(name))
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
