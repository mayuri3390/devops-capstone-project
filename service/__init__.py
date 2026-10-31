import sys
from flask import Flask
from flask_talisman import Talisman
from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Instantiate Talisman with security headers configuration
talisman = Talisman(app)

# Import routes and models
from service import routes, models  # noqa: F401, E402
from service.common import error_handlers  # noqa: F401, E402

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info("Service initialized successfully.")
