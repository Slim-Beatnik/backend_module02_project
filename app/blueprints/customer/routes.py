from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select

from app.extensions import cache, limiter

# app.models.get_all(table_class, many_schema)
from app.models import Customer, db, get_all
from app.utils.util import encode_token, role_required, token_required

from . import customer_bp
from .schemas import (
    creation_response_schema,
    customer_schema,
    login_schema,
    mechanic_view_customer_schema,
    mechanic_view_customers_schema,
)


@customer_bp.route("/login", methods=["POST"])
@limiter.limit("4 per 15 minutes")
def login():
    try:
        credentials = login_schema.load(request.json)
        username = credentials["email"]
        password = credentials["password"]
    except (KeyError, ValueError, ValidationError):
        return jsonify(
            {"error": "Invalid email or password!"},
        ), 401

    query = select(Customer).where(Customer.email == username)
    customer = db.session.execute(
        query,
    ).scalar_one_or_none()  # Query customer table for a customer with this email

    # soft deleted customers are not allowed to log in
    if not customer or (customer and customer.soft_delete):
        return jsonify({"error": "Invalid email or password!"}), 401

    # if we have a customer associated with the customername, validate the password
    if customer and customer.password == password:
        auth_token = encode_token(customer.id, "customer")

        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token,
        }
        return jsonify(response), 200
    return jsonify({"error": "Invalid email or password!"}), 401


@customer_bp.route("/", methods=["POST"])
@limiter.limit("5 per day")
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(
            {"message": f"{e.messages} - all customer data required."},
        ), 400

    query = select(Customer).where(
        Customer.email == customer_data["email"],
    )  # Checking our db for a customer with this email
    existing_customer = db.session.execute(query).one_or_none()

    # opted to handle potential IntegrityError with simple error handling
    if existing_customer:
        return jsonify({"error": "Email already associated with an account."}), 401

    new_customer = Customer(**customer_data)

    db.session.add(new_customer)
    db.session.commit()
    return creation_response_schema.jsonify(new_customer), 201


# ==================== CUSTOMER TOKEN REQUIRED =========================
@customer_bp.route("/", methods=["PUT"])
@limiter.limit("6 per day")
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 400

    try:
        customer_data = customer_schema.load(request.json)
        if not any(customer_data.values()):
            return jsonify({"message": "No changes made"}), 422
    except ValidationError as e:
        return jsonify(
            {"message": f"{e.messages} - all customer data fields required."},
        ), 400

    for key, value in customer_data.items():
        if value:
            setattr(customer, key, value)

    db.session.commit()
    return creation_response_schema.jsonify(customer), 200


# dummy delete, should also soft_delete if any service tickets are within the last tax-year
# should also soft delete if any service tickets associate with recallable inventory items with timedelta of 5 years of the service date
@customer_bp.route("/", methods=["DELETE"])
@limiter.limit("5 per day")
@token_required
def soft_delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    customer.soft_delete = True
    db.session.commit()
    return jsonify(
        {
            "message": "Customer successfully marked for deletion",
        },
    ), 200


@customer_bp.route("/my-account", methods=["GET"])
@token_required
def get_current_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer:
        return creation_response_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404


# ===================== MECHANIC/ADMIN TOKEN REQUIRED =====================
# needs admin blueprint, this should be protected by admin role
@customer_bp.route("/", methods=["GET"])
# @cache.cached(timeout=30)
@role_required
def get_customers():
    return get_all(Customer, mechanic_view_customers_schema)


# admin can look up customer by id
@customer_bp.route("/<int:customer_id>", methods=["GET"])
@cache.cached(timeout=10)
@role_required
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer:
        return mechanic_view_customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404
