import logging

def setup_logger():
    """
    Sets up the logger for JXYXSS.
    """
    logging.basicConfig(
        format='[%(asctime)s] [JXYXSS] [%(levelname)s]: %(message)s',
        level=logging.INFO
    )
    return logging.getLogger("JXYXSS")
