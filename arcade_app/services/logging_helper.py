import logging

logger = logging.getLogger("evalforge")


def debug_log(label: str, payload: any = None) -> None:
    logger.debug("%s: %s", label, payload)
