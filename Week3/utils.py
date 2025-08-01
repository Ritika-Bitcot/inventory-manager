import logging


def setup_logger(log_file: str = "errors.log"):
    """
    Set up a logger with the given file name
    that logs errors to that file.

    Args:
        log_file: The name of the file
        to log errors to. Defaults to "errors.log".
    """
    logging.basicConfig(filename=log_file, level=logging.ERROR, filemode="w")
