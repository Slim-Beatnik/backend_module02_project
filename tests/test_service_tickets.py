from datetime import date

from test_customer import SuperTest

from app.models import Customer, Inventory, Mechanics, ServiceTickets, db
from app.utils.util import encode_token


class TestInventory(SuperTest):
    def init_objects(self):
        self.customer1 = {
            "name": "kyle",
            "email": "kyle@gmail.com",
            "phone": "0123456789",
            "password": "test",
        }

        # consumables
        self.inventory1 = {
            "product_name": "High Milage Oil - HOUSE",
            "price": 15.43,
            "recallable": False,
        }
        self.inventory2 = {
            "product_name": "Regular Oil - HOUSE",
            "price": 12.24,
            "recallable": False,
        }
        # recallables
        self.inventory3 = {
            "product_name": "Tire - BRAND: Firestone",
            "price": 127.99,
        }
        self.inventory4 = {
            "product_name": "Tire - BRAND: Goodyear",
            "price": 127.99,
        }

        self.mechanics1 = {
            "name": "ed",
            "email": "ed@repairshop.com",
            "phone": "9719719711",
            "password": "test1",
            "salary": 199999.34,
        }
        self.mechanics2 = {
            "name": "edd",
            "email": "edd@repairshop.com",
            "phone": "5035035033",
            "password": "test2",
            "salary": 2.0,
        }

        self.service_ticket1 = {
            "customer_id": 1,
            "vin": "0123456789ABCEFGH",
            "service_desc": "Oil change and tire rotation",
            "service_date": date(2023, 10, 1),
        }

        with self.app.app_context():
            # convert customer1 to Customer object to enter into database
            db.session.add_all(
                [
                    Customer(**self.customer1),
                    Mechanics(**self.mechanics1),
                    Mechanics(**self.mechanics2),
                    Inventory(**self.inventory1),
                    Inventory(**self.inventory2),
                    Inventory(**self.inventory3),
                    Inventory(**self.inventory4),
                    ServiceTickets(**self.service_ticket1),
                ],
            )
            db.session.commit()
        self.customer1_header = {"Authorization": "Bearer " + encode_token(1)}
        self.mechanic1_header = {
            "Authorization": "Bearer " + encode_token(1, role="mechanic"),
        }
        self.client = self.app.test_client()

    # =========== CUSTOMER TOKEN REQUIRED =============
    def test_get_my_tickets(self):
        # add mechanics and inventory to service ticket
        self.client.put(
            "/service_tickets/1/edit-mechanics",
            json={"add_mechanic_ids": [1, 2], "remove_mechanic_ids": []},
            headers=self.mechanic1_header,
        )
        self.client.put(
            "/service_tickets/1/edit-inventory",
            json={"add_inventory_ids": [1], "remove_inventory_ids": []},
            headers=self.mechanic1_header,
        )

        # add service ticket 2 mechanics and inventory
        s2 = self.service_ticket1.copy()
        s2["service_desc"] = "New tire installation"
        s2["customer_id"] = 1

        with self.app.app_context():
            db.session.add(ServiceTickets(**s2))
            db.session.commit()

        self.client.put(
            "/service_tickets/2/edit-mechanics",
            json={"add_mechanic_ids": [1], "remove_mechanic_ids": []},
            headers=self.mechanic1_header,
        )
        self.client.put(
            "/service_tickets/2/edit-inventory",
            json={"add_inventory_ids": [4], "remove_inventory_ids": []},
            headers=self.mechanic1_header,
        )

        response = self.client.get(
            "/service_tickets/my-tickets",
            headers=self.customer1_header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(all("tire" in res["service_desc"] for res in response.json))
        self.assertEqual(len(response.json), 2)

    def test_create(self):
        s1 = self.service_ticket1.copy()
        s1["service_date"] = "2023-10-01"
        response = self.client.post(
            "/service_tickets/",
            json=s1,
            headers=self.mechanic1_header,
        )

        expected_response_obj = self.service_ticket1.copy()
        expected_response_obj["id"] = 2
        expected_response_obj["mechanics"] = []
        expected_response_obj["inventories"] = []
        expected_response_obj["service_date"] = "2023-10-01"

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(expected_response_obj, dict(response.json))

    def test_invalid_create(self):
        s1 = self.service_ticket1.copy()
        s1["service_date"] = "2023-10-01"
        del s1["service_desc"]

        response = self.client.post(
            "/service_tickets/",
            json=s1,
            headers=self.mechanic1_header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("- all service ticket fields required", response.json["message"])

    def test_get_all(self):
        s2 = self.service_ticket1.copy()
        s2["service_desc"] = "New tire installation"
        s2["customer_id"] = 1

        with self.app.app_context():
            db.session.add(ServiceTickets(**s2))
            db.session.commit()
        response = self.client.get("/service_tickets/", headers=self.mechanic1_header)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(all("tire" in res["service_desc"] for res in response.json))
        self.assertTrue(all(res["customer_id"] == 1 for res in response.json))
        self.assertEqual(len(response.json), 2)

    def test_get_all_paginated(self):
        s2 = self.service_ticket1.copy()
        s2["service_desc"] = "New tire installation"
        s2["customer_id"] = 1

        with self.app.app_context():
            db.session.add(ServiceTickets(**s2))
            db.session.commit()
        response = self.client.get(
            "/service_tickets/?page=2&per_page=1",
            headers=self.mechanic1_header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["service_desc"], "New tire installation")
        self.assertEqual(response.json[0]["customer_id"], 1)
        self.assertEqual(len(response.json), 1)

    def test_get_by_id(self):
        response = self.client.get("/service_tickets/1", headers=self.mechanic1_header)

        expected_response_obj = self.service_ticket1.copy()
        expected_response_obj["id"] = 1
        expected_response_obj["mechanics"] = []
        expected_response_obj["inventories"] = []
        expected_response_obj["service_date"] = "2023-10-01"

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_response_obj, dict(response.json))

    def test_invalid_get_by_id(self):
        response = self.client.get("/service_tickets/50", headers=self.mechanic1_header)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json["error"],
            "Service ticket not found.",
        )

    def test_edit_mechanics_assignments_by_service_ticket_id(self):
        response = self.client.put(
            "/service_tickets/1/edit-mechanics",
            json={"add_mechanic_ids": [1, 2], "remove_mechanic_ids": []},
            headers=self.mechanic1_header,
        )

        expected_response_obj = self.service_ticket1.copy()
        expected_response_obj["id"] = 1
        expected_response_obj["mechanics"] = [
            {"name": "ed", "email": "ed@repairshop.com", "phone": "9719719711"},
            {"name": "edd", "email": "edd@repairshop.com", "phone": "5035035033"},
        ]
        expected_response_obj["inventories"] = []
        expected_response_obj["service_date"] = "2023-10-01"

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_response_obj, dict(response.json))

    def test_edit_inventory_by_service_ticket_id(self):
        # include mechanic array to verify entire service ticket is returned
        self.client.put(
            "/service_tickets/1/edit-mechanics",
            json={"add_mechanic_ids": [1, 2], "remove_mechanic_ids": []},
            headers=self.mechanic1_header,
        )

        expected_response_obj = self.service_ticket1.copy()
        expected_response_obj["id"] = 1
        expected_response_obj["mechanics"] = [
            {"name": "ed", "email": "ed@repairshop.com", "phone": "9719719711"},
            {"name": "edd", "email": "edd@repairshop.com", "phone": "5035035033"},
        ]

        response = self.client.put(
            "/service_tickets/1/edit-inventory",
            json={"add_inventory_ids": [1, 2], "remove_inventory_ids": []},
            headers=self.mechanic1_header,
        )
        expected_response_obj["inventories"] = [
            {
                "product_name": "High Milage Oil - HOUSE",
                "price": 15.43,
            },
            {
                "product_name": "Regular Oil - HOUSE",
                "price": 12.24,
            },
        ]
        expected_response_obj["service_date"] = "2023-10-01"

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_response_obj, dict(response.json))

        # verify inventory can be removed w/o error
        response = self.client.put(
            "/service_tickets/1/edit-inventory",
            json={"add_inventory_ids": [], "remove_inventory_ids": [1]},
            headers=self.mechanic1_header,
        )
        expected_response_obj["inventories"] = [
            {
                "product_name": "Regular Oil - HOUSE",
                "price": 12.24,
            },
        ]

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_response_obj, dict(response.json))
