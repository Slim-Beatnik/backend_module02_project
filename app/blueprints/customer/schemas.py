from app.extensions import ma
from app.models import Customer


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

login_schema = CustomerSchema(only=("email", "password"))
creation_response_schema = CustomerSchema(exclude=("id", "soft_delete"))

mechanic_view_customer_schema = CustomerSchema(exclude=("password",))
mechanic_view_customers_schema = CustomerSchema(exclude=("password",), many=True)
