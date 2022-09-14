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
        self.test_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im9oYmljX2ZQZmhEcGIzSHBKODd2NCJ9.eyJpc3MiOiJodHRwczovL3JvYmVua3IudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYzMTlmOTk3OTY0ODUyZGQ3YTE4MzA2NSIsImF1ZCI6ImNvZmZlZXNob3AiLCJpYXQiOjE2NjMxOTc2OTIsImV4cCI6MTY2MzIwNDg5MiwiYXpwIjoiYklLS290UTVlYk1Cb2xiWWhRNUhqRnhERmkySzN0anoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.TRqhQqxB4EAFIjBcwVqQMGLsxsaKIAt5TSK4gEIXzgiSfrQlsh03pkhIcZBGofGC2PgTA_VvkGap8BgqZdMbee048h5WD-9exrZYEcjzI8QOfpfw_3YS9ZdC5p_PYJvBLIJkvNh-30Lc9s07gpiwKPqDgj7beO9WDqU7fK8r2r2IE-hcy_JNvdhrS6mjcVQFP9uU_hzylac1I73euhRqtl69xlsmIB7fGso31hig4LbG9l6CCrvaTb-azZxcECpkAZ6Gof4gUcK0vBFpZaQKZ-bC9kREzfvkQ9n-jTwGntdMYxy8A1xiKQ1AN1dXyjZps3rcrBnc35NbIUnIZB4Fwg'

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

    def test_401_delete_drink(self):
        res = self.client().delete(
            'drinks/33',
            headers={
                'Authorization': self.test_token,
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

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


if __name__ == '__main__':
    unittest.main()
