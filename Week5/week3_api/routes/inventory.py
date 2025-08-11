from flask import Blueprint, jsonify

inventory_bp = Blueprint("inventory", __name__)


# note url will be /api/hello
@inventory_bp.route("/hello", methods=["GET"])
def hello():
    """
    Simple hello endpoint to confirm blueprint setup.
    """
    return jsonify({"message": "Hello from Inventory API!"}), 200
