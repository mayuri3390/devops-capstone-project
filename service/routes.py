from flask import jsonify, request, url_for, abort
from service.models import Account
from service.common import status
from . import app


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), status.HTTP_200_OK


@app.route("/")
def index():
    return jsonify(name="Account REST API Service", version="1.0"), status.HTTP_200_OK


@app.route("/accounts", methods=["POST"])
def create_accounts():
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    location_url = url_for("get_accounts", account_id=account.id, _external=True)
    return jsonify(account.serialize()), status.HTTP_201_CREATED, {"Location": location_url}


@app.route("/accounts", methods=["GET"])
def list_accounts():
    accounts = Account.all()
    return jsonify([a.serialize() for a in accounts]), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    return jsonify(account.serialize()), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    account.deserialize(request.get_json())
    account.update()
    return jsonify(account.serialize()), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", status.HTTP_204_NO_CONTENT


def check_content_type(media_type):
    if request.headers.get("Content-Type") != media_type:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {media_type}")
