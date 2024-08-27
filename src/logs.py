import logging


def set_log_verbosity(verbosity: int):
    log_levels = [logging.ERROR, logging.WARNING, logging.INFO]
    logging.basicConfig(
        format="%(levelname)s: %(message)s", level=log_levels[verbosity]
    )
