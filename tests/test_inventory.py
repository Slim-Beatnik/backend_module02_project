from test_customer import SuperTest

from app.models import Customer, Inventory, Mechanics, db
from app.utils.util import encode_token


class TestInventory(SuperTest):
    def init_objects(self):
        self.mechanics1 = {
            "name": "ed",
            "email": "ed@repairshop.com",
            "phone": "9719719711",
            "password": "test1",
            "salary": 199999.34,
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

        self.customer1 = {
            "name": "kyle",
            "email": "kyle@gmail.com",
            "phone": "0123456789",
            "password": "test",
        }

        with self.app.app_context():
            # convert customer1 to Customer object to enter into database
            db.session.add_all(
                [
                    Customer(**self.customer1),
                    Mechanics(**self.mechanics1),
                    Inventory(**self.inventory1),
                    Inventory(**self.inventory3),
                    Inventory(**self.inventory4),
                ],
            )
            db.session.commit()
        self.token1 = encode_token(1)
        self.mechanic_token1 = encode_token(1, role="mechanic")
        self.client = self.app.test_client()

    # =========== UNPROTECTED SHOP ROUTES =============
    def test_shop_get_all(self):
        # no header required
        response = self.client.get("/inventory/shop")

        # inventory schema for customers only includes name and price
        # make copies and remove recallable key
        i1 = self.inventory1.copy()
        del i1["recallable"]

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(i1, dict(response.json[0]))
        self.assertDictEqual(self.inventory3, dict(response.json[1]))
        self.assertDictEqual(self.inventory4, dict(response.json[2]))

    def test_shop_get_product_by_id(self):
        response = self.client.get("/inventory/shop/product/1")
        i1 = self.inventory1.copy()
        del i1["recallable"]

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(i1, dict(response.json))

    def test_shop_search_name(self):
        response = self.client.get("/inventory/shop/search?name=oil")
        i1 = self.inventory1.copy()
        del i1["recallable"]
        self.assertEqual(response.status_code, 200)
        self.assertIn(i1, response.json)

    # ========= MECHANIC TOKEN REQUIRED ================
    def test_create(self):
        header = {"Authorization": "Bearer " + self.mechanic_token1}
        inventory_payload = self.inventory2

        response = self.client.post(
            "/inventory/",
            json=inventory_payload,
            headers=header,
        )

        expected_response_obj = self.inventory2.copy()
        expected_response_obj["recallable"] = False
        expected_response_obj["id"] = 4
        expected_response_obj["no_longer_used"] = False
        expected_response_obj["recalled"] = False

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(expected_response_obj, dict(response.json))

    def test_invalid_create(self):
        header = {"Authorization": "Bearer " + self.mechanic_token1}
        inventory_payload = self.inventory2["product_name"]

        response = self.client.post(
            "/inventory/",
            json=inventory_payload,
            headers=header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("- all inventory fields required", response.json["message"])

    def test_get_inventory_by_id(self):
        header = {"Authorization": "Bearer " + self.mechanic_token1}

        response = self.client.get("/inventory/1", headers=header)
        expected_response_obj = self.inventory1.copy()
        expected_response_obj["recallable"] = False
        expected_response_obj["id"] = 1
        expected_response_obj["no_longer_used"] = False
        expected_response_obj["recalled"] = False

        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response_obj, dict(response.json))

    def test_invalid_get_inventory_by_id(self):
        header = {"Authorization": "Bearer " + self.mechanic_token1}

        response = self.client.get("/inventory/25", headers=header)
        self.assertEqual(response.status_code, 404)

    def test_get_all(self):
        header = {"Authorization": "Bearer " + self.mechanic_token1}
        response = self.client.get("/inventory/", headers=header)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json[0]["product_name"])

    def test_customer_token_get_all(self):
        header = {"Authorization": "Bearer " + self.token1}
        response = self.client.get("/inventory/", headers=header)

        self.assertEqual(response.status_code, 403)

    def test_delete_by_id(self):
        header = {"Authorization": "Bearer " + self.mechanic_token1}
        response = self.client.delete("/inventory/1", headers=header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["message"],
            "Inventory item id: 1, successfully set to no_longer_used.",
        )

    def test_invalid_delete_by_id(self):
        header = {"Authorization": "Bearer " + self.mechanic_token1}
        response = self.client.delete("/inventory/50", headers=header)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json["error"],
            "Inventory item not found.",
        )

    def test_get_all_current(self):
        header = {"Authorization": "Bearer " + self.mechanic_token1}
        # set inventory id: 1 property no_longer_used to True
        self.client.delete("/inventory/1", headers=header)

        response = self.client.get("/inventory/current", headers=header)

        # verify 200 code sent, and object with no_longer_used name doesn't appear in response name values
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            "High Milage Oil - HOUSE",
            [inv_obj["product_name"] for inv_obj in response.json],
        )

    def test_get_all_search(self):
        header = {"Authorization": "Bearer " + self.mechanic_token1}
        # set inventory id: 1 property no_longer_used to True
        self.client.delete("/inventory/1", headers=header)

        response = self.client.get(
            "/inventory/search?na=0",
            headers=header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            "High Milage Oil - HOUSE",
            [inv_obj["product_name"] for inv_obj in response.json],
        )

        response2 = self.client.get(
            "/inventory/search?name=oil",
            headers=header,
        )

        self.assertIn(
            "High Milage Oil - HOUSE",
            [inv_obj["product_name"] for inv_obj in response2.json],
        )

    def test_no_query_search(self):
        header = {"Authorization": "Bearer " + self.mechanic_token1}
        response = self.client.get("/inventory/search", headers=header)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json["message"],
            "No search parameters provided.",
        )

    def test_put(self):
        header = {"Authorization": "Bearer " + self.mechanic_token1}

        update_payload = {"product_name": "", "price": 14.00}

        expected_updated_obj = {
            "id": 1,
            "product_name": "High Milage Oil - HOUSE",
            "price": 14.0,
            "recalled": False,
            "recallable": False,
            "no_longer_used": False,
        }
        response = self.client.put("/inventory/1", json=update_payload, headers=header)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expected_updated_obj, dict(response.json))

    def test_invalid_put(self):
        header = {"Authorization": "Bearer " + self.mechanic_token1}

        update_payload = {"price": 14.00}

        response = self.client.put("/inventory/1", json=update_payload, headers=header)

        self.assertEqual(response.status_code, 400)
        self.assertIn("- all inventory fields required.", response.json["message"])
