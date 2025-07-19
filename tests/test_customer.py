import gc
import unittest

from app import create_app
from app.models import Customer, Mechanics, db
from app.utils.util import encode_token


class SuperTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()
        self.init_objects()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()
        gc.collect()


class TestCustomer(SuperTest):
    def init_objects(self):
        self.customer1 = {
            "name": "kyle",
            "email": "kyle@gmail.com",
            "phone": "0123456789",
            "password": "test",
        }

        self.updated_customer1 = {
            "name": "Kyle",  # changed to uppercase
            "email": "",
            "phone": "9876543210",  # changed phone number
            "password": "",
        }

        self.customer2 = {
            "name": "rev",
            "email": "rev@gmail.com",
            "phone": "1234567890",
            "password": "test",
        }

        self.mechanic1 = {
            "name": "ed",
            "email": "ed@repairshop.com",
            "phone": "9719719711",
            "password": "test1",
            "salary": 199999.34,
        }

        with self.app.app_context():
            # convert customer1 to Customer object to enter into database
            customer1_obj = Customer(**self.customer1)
            mechanic1_obj = Mechanics(**self.mechanic1)
            db.session.add_all([customer1_obj, mechanic1_obj])
            db.session.commit()
        self.token1 = encode_token(1)
        self.mechanic_token1 = encode_token(1, role="mechanic")
        self.client = self.app.test_client()

    # =============== UNPROTECTED - BUT LIMITED ============================
    def test_create(self):
        customer_payload = self.customer2
        response = self.client.post("/customers/", json=customer_payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], customer_payload["name"])

    def test_existing_create(self):
        customer_payload = self.customer1
        response = self.client.post("/customers/", json=customer_payload)

        self.assertEqual(response.status_code, 401)
        self.assertIn("already", response.json["error"])

    def test_login(self):
        login_payload = {
            "email": self.customer1["email"],
            "password": self.customer1["password"],
        }
        response = self.client.post("/customers/login", json=login_payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

    def test_invalid_creation(self):
        # payload missing email field
        incomplete_payload = {
            "name": "kyle",
            "phone": "1234567890",
            "password": "test",
        }
        response = self.client.post("/customers/", json=incomplete_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("all customer data required", response.json["message"])

    def test_invalid_login(self):
        login_payload = {
            "email": self.customer1["email"],
        }
        response = self.client.post("/customers/login", json=login_payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual("Invalid email or password!", response.json["error"])

    # =================== CUSTOMER TOKEN PROTECTED ===========================
    def test_update(self):
        updated_payload = {
            "name": "Kyle",  # changed to uppercase
            "email": "",  # blank strings falsy and aren't reassigned
            "phone": "9876543210",  # changed phone number
            "password": "",
        }

        customer1_header = {"Authorization": "Bearer " + self.token1}

        response = self.client.put(
            "/customers/",
            json=updated_payload,
            headers=customer1_header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], self.updated_customer1["name"])
        self.assertEqual(response.json["phone"], "9876543210")

    def test_invalid_update(self):
        # missing email field
        incomplete_payload = {
            "name": "Kyle",
            "phone": "9876543210",
            "password": "",
        }

        customer1_header = {"Authorization": "Bearer " + self.token1}

        response = self.client.put(
            "/customers/", json=incomplete_payload, headers=customer1_header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("all customer data fields required.", response.json["message"])

    def test_delete(self):
        customer2_obj = Customer(**self.customer2)
        with self.app.app_context():
            db.session.add(customer2_obj)
            db.session.commit()

        token2 = encode_token(2)
        customer2_header = {"Authorization": "Bearer " + token2}

        response = self.client.delete("/customers/", headers=customer2_header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"], "Customer successfully marked for deletion",
        )

    def test_get(self):
        customer2_obj = Customer(**self.customer2)
        with self.app.app_context():
            db.session.add(customer2_obj)
            db.session.commit()

        token2 = encode_token(2)
        customer2_header = {"Authorization": "Bearer " + token2}

        response = self.client.get("/customers/my-account", headers=customer2_header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "rev")

    # ========================= MECHANIC TOKEN PROTECTED ==============================
    def test_mechanic_get_all(self):
        customer2_obj = Customer(**self.customer2)
        with self.app.app_context():
            db.session.add(customer2_obj)
            db.session.commit()
        mechanic1_header = {"Authorization": "Bearer " + self.mechanic_token1}

        response = self.client.get("/customers/", headers=mechanic1_header)

        # remove password and add id and soft_delete fields to match mechanic_view_customers_schema output
        del self.customer1["password"]
        self.customer1["id"] = 1
        self.customer1["soft_delete"] = False

        del self.customer2["password"]
        self.customer2["id"] = 2
        self.customer2["soft_delete"] = False

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.customer1, dict(response.json[0]))
        self.assertEqual(self.customer2, dict(response.json[1]))

    def test_mechanic_get_all_paginated(self):
        customer2_obj = Customer(**self.customer2)
        with self.app.app_context():
            db.session.add(customer2_obj)
            db.session.commit()
        mechanic1_header = {"Authorization": "Bearer " + self.mechanic_token1}

        # paginated to view customers 1 at a time, only page 2
        response = self.client.get(
            "/customers/?page=2&per_page=1", headers=mechanic1_header,
        )

        # remove password and add id and soft_delete fields to match mechanic_view_customers_schema output
        del self.customer2["password"]
        self.customer2["id"] = 2
        self.customer2["soft_delete"] = False

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.customer2, dict(response.json[0]))

    # def test_mechanic_get_customer
    def test_mechanic_get_by_id(self):
        mechanic1_header = {"Authorization": "Bearer " + self.mechanic_token1}

        response = self.client.get("/customers/1", headers=mechanic1_header)

        # remove password and add id and soft_delete fields to match mechanic_view_customer_schema output
        del self.customer1["password"]
        self.customer1["id"] = 1
        self.customer1["soft_delete"] = False

        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict(response.json), self.customer1)
