import logging


def init_logger(name):
    logger = logging.getLogger(name)
    fh = logging.FileHandler('logs/{}.log'.format(name))
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
