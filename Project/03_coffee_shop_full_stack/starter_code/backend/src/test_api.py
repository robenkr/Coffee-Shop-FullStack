import json
import unittest
import os
from .api import app
from .database.models import setup_db, db_drop_and_create_all, Drink


class CoffeeShopTestCase(unittest.TestCase):
    def setUp(self) -> None:
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client

        setup_db(self.app)

        self.new_drink = {
            'title': 'Chilli light',
            'recipe': [
                {
                    'name': 'chilli',
                    'color': 'red',
                    'parts': 1
                },
                {
                    'name': 'sugar',
                    'color': 'blue',
                    'parts': 2
                },
                {
                    'name': 'wine',
                    'color': 'gray',
                    'parts': 1
                }
            ]
        }
        self.update_drink = {
            'title': 'Chilli Soda'
        }
        self.test_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im9oYmljX2ZQZmhEcGIzSHBKODd2NCJ9.eyJpc3MiOiJodHRwczovL3JvYmVua3IudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYzMTlmOTk3OTY0ODUyZGQ3YTE4MzA2NSIsImF1ZCI6ImNvZmZlZXNob3AiLCJpYXQiOjE2NjM0MzMwMzMsImV4cCI6MTY2MzUxOTQzMywiYXpwIjoiYklLS290UTVlYk1Cb2xiWWhRNUhqRnhERmkySzN0anoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.IdtPPTO-wne-MQKhAd-KI-VdL9q5xMbHRwIMZXAaUvsag-ZN7-tVUPkR_sVq9IILwRK20q9aSWaZmrFdKXDCDjJ27zBFG6ZuTUq9ioWyU3opX1qdYYd8rBeqcqezO5YcMnpgzp1265LaodqHKQ5sSbgiUCkEz9jaj1t1319pH1Qf6p7VvgWw6ZHNOYhcwOxiTL-7L9ChJ9cV2aJEI8A5kA7TrXDkdrNFS0HlX3n09eNkk6JBSWivtkBfeU-Csjl06agPDoVOHVS7KKk7Wjswq6BG5f1qf46NfcMkLKpWWV6K3IthBp4o6MsEDh-Yzq2enArHTDPW2ClyjOwMUWhapA'

    with app.app_context():
        db_drop_and_create_all()

        drink2 = Drink(
            title='green-belt',
            recipe='[{"name": "green-belt", "color": "green", "parts": 1}]'
        )
        drink3 = Drink(
            title='water7',
            recipe='[{"name": "water7", "color": "skyblue", "parts": 1}]'
        )

        drink2.insert()
        drink3.insert()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_drinks(self):
        res = self.client().get('drinks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['drinks']))

    def test_get_drinks_detail(self):
        res = self.client().get(
            'drinks-detail',
            headers={
                'Authorization': self.test_token,
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['drinks']))

    def test_delete_drink(self):
        res = self.client().delete(
            'drinks/1',
            headers={
                'Authorization': self.test_token,
            },
        )
        data = json.loads(res.data)

        drink = Drink.query.filter(Drink.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(drink, None)

    def test_404_delete_drink(self):
        res = self.client().delete(
            'drinks/33',
            headers={
                'Authorization': self.test_token,
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_drinks(self):
        res = self.client().post(
            'drinks',
            json= self.new_drink,
            headers={
                'Authorization': self.test_token,
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['drinks']))

    def test_update_drink(self):
        res = self.client().patch(
            'drinks/2',
            json= self.update_drink,
            headers={
                'Authorization': self.test_token,
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['drinks']))


if __name__ == '__main__':
    unittest.main()
