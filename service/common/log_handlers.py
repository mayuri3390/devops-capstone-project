import logging


def init_logging(app, logger_name):
    gunicorn_logger = logging.getLogger(logger_name)
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s", "%Y-%m-%d %H:%M:%S %z"
    )
    for handler in app.logger.handlers:
        handler.setFormatter(formatter)
