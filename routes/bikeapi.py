import json
import os
from functools import wraps

from flask import Blueprint, request, jsonify
from cloudinary.uploader import upload

from app import db
from models.bike import Bike
import requests

bikeapi_bp = Blueprint('bikeapi', __name__)


# await axios.post(
#         `https://www.google.com/recaptcha/api/siteverify?secret=${secret}&response=${response}`,
#         {},
#         {
#             headers: {
#                 "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
#             }
#         }
#     )
#     console.log(data)
#     const {success} = data;
def with_auth(f):
    @wraps(f)
    def before_request(*args, **kwargs):
        if request.access_control_request_method == "OPTIONS":
            return f(*args, **kwargs)
        token = request.headers.get("x-token")
        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify?secret={secret}&response={response}".format(
                secret=os.getenv("RECAPTCHA_SECRET"),
                response=token
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
            }
        ).json()
        if response.get("success"):
            return f(*args, **kwargs)
        return "Not Found", 400

    return before_request


@bikeapi_bp.route("/files", methods=["POST"])
@with_auth
def upload_file():
    file = request.files['file']
    uploaded_file = upload(file)
    res = dict(
        message="success",
        file=dict(
            asset_id=uploaded_file.get("asset_id"),
            name=file.filename
        )
    )
    return jsonify(res)


@bikeapi_bp.route("/bike", methods=["POST"])
@with_auth
def create_bike():
    content = request.json
    if db.session.query(Bike).filter(Bike.bike_id == content.get("bikeDetails", {}).get("bike_id")).first():
        return jsonify({
            "error": {"bike_id": "already exists"}
        })
    bike_details = content.get("bikeDetails")
    b = Bike(
        first_name=bike_details.get("firstName"),
        last_name=bike_details.get("lastName"),
        color=bike_details.get("color"),
        brand=bike_details.get("brand"),
        phone=bike_details.get("phone"),
        city=bike_details.get("city"),
        secondary_phone=bike_details.get("secondary_phone"),
        bike_id=bike_details.get("bike_id"),
        assets=json.dumps(bike_details.get("assets")),
    )
    db.session.add(b)
    db.session.commit()
    bike = b
    res = dict(
        brand=bike.brand,
        color=bike.color,
        bike_id=bike.bike_id,
        firstName=bike.first_name,
        lastName=bike.last_name,
        city=bike.city,
        phone=bike.phone,
        secondary_phone=bike.secondary_phone,
    )
    return jsonify({"success": True, "result": {
        "bike": res}
    })


@bikeapi_bp.route("/bike/<bike_id>", methods=["GET"])
@with_auth
def search_bikes(bike_id):
    bike = db.session.query(Bike).filter(Bike.bike_id == bike_id).first()
    if not bike:
        return jsonify({"result": {}})
    return jsonify({
        "result": {"bike": dict(
            brand=bike.brand,
            color=bike.color,
            bike_id=bike.bike_id,
            firstName=bike.first_name,
            lastName=bike.last_name,
            city=bike.city,
            phone=bike.phone,
            secondary_phone=bike.secondary_phone,
        )
        }})
