from datetime import date

from test_customer import SuperTest

from app.models import Customer, Mechanics, ServiceTickets, db
from app.utils.util import encode_token


class TestMechanics(SuperTest):
    def init_objects(self):
        self.mechanics1 = {
            "name": "ed",
            "email": "ed@repairshop.com",
            "phone": "9719719711",
            "password": "test1",
            "salary": 199999.34,
        }

        self.updated_mechanics1 = {
            "name": "ed",  # changed to uppercase
            "email": "",
            "phone": "9289289280",  # changed phone number
            "password": "",
            "salary": 0,
        }

        self.mechanics2 = {
            "name": "test_name",
            "email": "test@repairshop.com",
            "phone": "5035035033",
            "password": "test2",
            "salary": 2.00,
        }

        self.mechanic3 = {
            "name": "edd",
            "email": "edd@repairshop.com",
            "phone": "1234567890",
        }

        self.customer1 = {
            "name": "kyle",
            "email": "kyle@gmail.com",
            "phone": "0123456789",
            "password": "test",
        }

        with self.app.app_context():
            # convert customer1 to Customer object to enter into database
            customer1_obj = Customer(**self.customer1)
            mechanics1_obj = Mechanics(**self.mechanics1)
            db.session.add_all([customer1_obj, mechanics1_obj])
            db.session.commit()
        self.token1 = encode_token(1)
        self.mechanic_token1 = encode_token(1, role="mechanic")
        self.client = self.app.test_client()

    # =============== UNPROTECTED ============================
    def test_create(self):
        mechanics_payload = self.mechanics2
        response = self.client.post("/mechanics/", json=mechanics_payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], mechanics_payload["name"])

    def test_existing_create(self):
        # First post, should succeed
        self.client.post(
            "/mechanics/",
            json={
                "name": "Ed",
                "email": "ed@repairshop.com",
                "phone": "1234567890",
                "password": "test123",
                "salary": 100000.00,
            },
        )

        # Second post with same email, should trigger 400
        response = self.client.post(
            "/mechanics/",
            json={
                "name": "Edd",
                "email": "ed@repairshop.com",  # duplicate email
                "phone": "0987654321",
                "password": "test456",
                "salary": 120000.00,
            },
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json["error"], "Email already associated with an account."
        )

    def test_login(self):
        login_payload = {
            "email": self.mechanics1["email"],
            "password": self.mechanics1["password"],
        }
        response = self.client.post("/mechanics/login", json=login_payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

    def test_invalid_login(self):
        incomplete_payload = {
            "email": self.mechanics1["email"],
        }
        response = self.client.post("/mechanics/login", json=incomplete_payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Username and password required.", response.json["messages"])

    def test_mechanic_creation(self):
        mechanic_payload = self.mechanics2

        response = self.client.post("/mechanics/", json=mechanic_payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], mechanic_payload["name"])

    def test_invalid_creation(self):
        # payload missing email field
        incomplete_payload = {
            "name": "kyle",
            "phone": "1234567890",
            "password": "test",
        }

        response = self.client.post("/mechanics/", json=incomplete_payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("- all mechanic data required.", response.json["message"])

    # =================== MECHANICS TOKEN PROTECTED ===========================
    def test_update(self):
        update_payload = {
            "name": "Edward",  # changed to Edward
            "email": "",  # blank strings falsy and aren't reassigned
            "phone": "1010101010",  # changed phone number
            "password": "",
            "salary": 0,  # will evaluate as false
        }

        mechanics1_header = {"Authorization": "Bearer " + self.mechanic_token1}

        response = self.client.put(
            "/mechanics/1",
            json=update_payload,
            headers=mechanics1_header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], update_payload["name"])
        self.assertEqual(response.json["phone"], "1010101010")

    def test_invalid_update(self):
        # missing email field
        incomplete_payload = {
            "name": "Kyle",
            "phone": "9876543210",
            "password": "",
        }

        mechanics1_header = {"Authorization": "Bearer " + self.mechanic_token1}

        response = self.client.put(
            "/mechanics/1",
            json=incomplete_payload,
            headers=mechanics1_header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("all mechanic data fields required", response.json["message"])

    def test_no_change_update(self):
        devalued_payload = {
            "name": "",  # changed to Edward
            "email": "",  # blank strings falsy and aren't reassigned
            "phone": "",  # changed phone number
            "password": "",
            "salary": 0,  # will evaluate as false
        }

        mechanics1_header = {"Authorization": "Bearer " + self.mechanic_token1}

        response = self.client.put(
            "/mechanics/1",
            json=devalued_payload,
            headers=mechanics1_header,
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json["message"], "No changes made")

    def test_delete(self):
        mechanics2_obj = Mechanics(**self.mechanics2)
        with self.app.app_context():
            db.session.add(mechanics2_obj)
            db.session.commit()

        token2 = encode_token(2, "mechanic")
        mechanics2_header = {"Authorization": "Bearer " + token2}

        response = self.client.delete("/mechanics/2", headers=mechanics2_header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            "Mechanic id: 2, successfully deleted.",
        )

    def test_invalid_delete(self):
        header = {"Authorization": "Bearer " + self.mechanic_token1}

        response = self.client.delete("/mechanics/20", headers=header)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Mechanic not found.")

    def test_get_all(self):
        mechanics2_obj = Mechanics(**self.mechanics2)
        with self.app.app_context():
            db.session.add(mechanics2_obj)
            db.session.commit()

        token2 = encode_token(2, "mechanic")
        mechanics2_header = {"Authorization": "Bearer " + token2}

        response = self.client.get("/mechanics/", headers=mechanics2_header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[1]["name"], "test_name")
        self.assertEqual(response.json[0]["name"], "ed")

    def test_invalid_token_get(self):
        customer_token = encode_token(1)
        bad_header = {"Authorization": "Bearer " + customer_token}

        response = self.client.get("/mechanics/", headers=bad_header)

        self.assertEqual(response.status_code, 403)

    def test_get_current_customers_search_email(self):
        customer2_obj = Customer(
            name="name",
            password="password",
            phone="1234567890",
            email="unique@email.com",
        )
        with self.app.app_context():
            db.session.add(customer2_obj)
            db.session.commit()

        header = {"Authorization": "Bearer " + self.mechanic_token1}

        response = self.client.get(
            "/mechanics/current-customer-search?email=.com",
            headers=header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"][0]["name"], "kyle")
        self.assertEqual(response.json["result"][1]["name"], "name")

    def test_get_current_customers_search_name(self):
        customer2_obj = Customer(
            name="name",
            password="password",
            phone="1234567890",
            email="unique@email.com",
        )
        with self.app.app_context():
            db.session.add(customer2_obj)
            db.session.commit()

        header = {"Authorization": "Bearer " + self.mechanic_token1}

        response = self.client.get(
            "/mechanics/current-customer-search?name=name",
            headers=header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"][0]["name"], "name")
        self.assertEqual(len(response.json["result"]), 1)

    def test_get_current_customers_search_any(self):
        customer2_obj = Customer(
            name="name",
            password="password",
            phone="1234567890",
            email="unique@email.com",
        )
        with self.app.app_context():
            db.session.add(customer2_obj)
            db.session.commit()

        header = {"Authorization": "Bearer " + self.mechanic_token1}

        response = self.client.get(
            "/mechanics/current-customer-search?any=captain_smarty-pants",
            headers=header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], [])
        self.assertEqual(response.json["message"], "Filters failed to yield results.")

    def test_get_deleted_customers_search(self):
        customer2_obj = Customer(
            name="name",
            password="password",
            phone="1234567890",
            email="unique@email.com",
        )
        with self.app.app_context():
            db.session.add(customer2_obj)
            db.session.get(Customer, 1).soft_delete = True
            db.session.commit()

        header = {"Authorization": "Bearer " + self.mechanic_token1}

        response = self.client.get(
            "/mechanics/deleted-customer-search?email=.com",
            headers=header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"][0]["email"], "kyle@gmail.com")

    def test_get_top_mechanics(self):
        # service ticket data
        st1 = {
            "vin": "abcdefghijklmnop1",
            "service_date": date(2025, 1, 20),
            "service_desc": "some stuff",
            "customer_id": 1,
        }
        st2 = {
            "vin": "abcdefghijklmnop1",
            "service_date": date(2025, 1, 20),
            "service_desc": "other stuff",
            "customer_id": 1,
        }
        st3 = {
            "vin": "abcdefghijklmnop1",
            "service_date": date(2025, 1, 20),
            "service_desc": "some thing",
            "customer_id": 1,
        }
        st4 = {
            "vin": "abcdefghijklmnop1",
            "service_date": date(2025, 1, 20),
            "service_desc": "some else",
            "customer_id": 1,
        }
        # mechanic data
        m2 = {
            "name": "edd",
            "phone": "2222222222",
            "email": "edd@repairshop.com",
            "password": "test2",
            "salary": 2,
        }
        m3 = {
            "name": "eddy",
            "phone": "3333333333",
            "email": "eddy@repairshop.com",
            "password": "test3",
            "salary": 3,
        }
        m4 = {
            "name": "Neadore",
            "phone": "4444444444",
            "email": "Neadore@repairshop.com",
            "password": "test4",
            "salary": 4,
        }

        # service tickets and mechanics need to be added
        with self.app.app_context():
            db.session.add_all(
                [ServiceTickets(**st) for st in (st1, st2, st3, st4)]
                + [Mechanics(**mechanic) for mechanic in (m2, m3, m4)],
            )
            db.session.commit()
        header = {"Authorization": "Bearer " + self.mechanic_token1}

        # assign mechanics to service tickets by id data
        data_input1 = {"add_mechanic_ids": [1, 2, 4], "remove_mechanic_ids": []}
        data_input2 = {"add_mechanic_ids": [1, 2, 3], "remove_mechanic_ids": []}
        data_input3 = {"add_mechanic_ids": [1, 2, 4], "remove_mechanic_ids": []}
        data_input4 = {"add_mechanic_ids": [1], "remove_mechanic_ids": []}

        # send data to update mechanics assigned to service tickets by id
        self.client.put(
            "/service_tickets/1/edit-mechanics",
            json=data_input1,
            headers=header,
        )
        self.client.put(
            "/service_tickets/2/edit-mechanics",
            json=data_input2,
            headers=header,
        )
        self.client.put(
            "/service_tickets/3/edit-mechanics",
            json=data_input3,
            headers=header,
        )
        self.client.put(
            "/service_tickets/4/edit-mechanics",
            json=data_input4,
            headers=header,
        )

        response = self.client.get("/mechanics/top-mechanics")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Neadore", response.json["3"]["name"])

        # Verify key exists when limit is increased
        response2 = self.client.get("/mechanics/top-mechanics?limit=4")
        self.assertIsNotNone(response2.json.get("4", None))
