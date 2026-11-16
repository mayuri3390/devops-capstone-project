from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from service import config
from service.common import log_handlers

app = Flask(__name__)
app.config.from_object(config)

talisman = Talisman(app)
CORS(app)

from service import routes, models  # noqa: F401, E402
from service.common import error_handlers  # noqa: F401, E402

log_handlers.init_logging(app, "gunicorn.error")
app.logger.info("Service initialized successfully.")
