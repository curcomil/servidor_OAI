from flask import Blueprint, request
from controllers import identify

oai_bp = Blueprint("oai", __name__)

@oai_bp.route("/", methods=["GET"])
def oai_root():
    verb = request.args.get("verb")

    if not verb:
        return {"error": "Missing required parameter verb"}, 400
    
    if verb == "Identify":
        return identify()
