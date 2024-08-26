import logging as log


def get_log(verbosity: int):
    log_levels = [log.ERROR, log.WARNING, log.INFO]
    log.basicConfig(format="%(levelname)s: %(message)s", level=log_levels[verbosity])
    return log
