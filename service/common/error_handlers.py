from flask import jsonify
from service import app
from service.models import DataValidationError
from service.common import status


@app.errorhandler(DataValidationError)
def request_validation_error(error):
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    return jsonify(status=400, error="Bad Request", message=str(error)), 400


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    return jsonify(status=404, error="Not Found", message=str(error)), 404


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    return jsonify(status=405, error="Method not Allowed", message=str(error)), 405


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    return jsonify(status=415, error="Unsupported media type", message=str(error)), 415
