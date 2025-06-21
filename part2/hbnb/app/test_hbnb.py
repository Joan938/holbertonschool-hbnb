import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    
    def tearDown(self):
        if hasattr(self, 'email'):
            self.client.delete(f'/api/v1/users/')


    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jake",
            "last_name": "Gates",
            "email": "jake.gates@example.com"
        })
        self.assertEqual(response.status_code, 201)


    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "Invalid-email"
        })
        self.assertEqual(response.status_code, 400)


    def test_get_all_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)


class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Foster",
            "email": "jane.foster@example.com"
        })
        user = user_response.get_json()
        if 'id' in user:
            self.user_id = user['id']
        else:
            self.user_id = None
        response = self.client.post('/api/v1/places/', json={
            "title": "Mountain Villa",
            "description": "A amazing Mountain property",
            "price": 200.50,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner": {"id": self.user_id}
        })
        self.assertEqual(response.status_code, 201)
        place = response.get_json()
        self.assertIn('id', place)
        self.place_id = place['id']


    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Moutain Villa",
            "description": "A amazing Mountain property",
            "price": 200.50,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner": {"id": self.user_id}
        })
        self.assertEqual(response.status_code, 201)


    def test_get_place_by_id(self):
        response = self.client.get(f'/api/v1/places/{self.place_id}')
        self.assertEqual(response.status_code, 200)


    def test_get_all_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)


class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Swimming Pool"
        })
        amenity = response.get_json()
        self.assertIn('id', amenity)
        self.amenity_id = amenity["id"]


    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Swimming Pool"
        })
        self.assertEqual(response.status_code, 201)


    def test_get_amenity_by_id(self):
        response = self.client.get(f'/api/v1/amenities/{self.amenity_id}')
        self.assertEqual(response.status_code, 200)


    def test_get_all_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)


    def test_update_amenity(self):
        response = self.client.put(f'/api/v1/amenities/{self.amenity_id}', json={
            "name": "WI-FI"
        })
        self.assertEqual(response.status_code, 200)


class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Victor",
            "last_name": "Sanders",
            "email": "victor.sanders@example.com"
        })
        print(f"User creation response: {user_response.status_code}, {user_response.get_json()}")
        user = user_response.get_json()
        self.user_id = user.get("id")
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Mountain Villa",
            "description": "A amazing Mountain property",
            "price": 200.50,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner": {"id": self.user_id}
        })
        print(f"Place creation response: {place_response.status_code}, {place_response.get_json()}")
        self.assertEqual(place_response.status_code, 201)
        place = place_response.get_json()
        self.place_id = place.get("id")
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        review = response.get_json()
        self.review_id = review.get("id")


    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)


    def test_get_review_by_id(self):
        response = self.client.get(f'/api/v1/reviews/{self.review_id}')
        self.assertEqual(response.status_code, 200)


    def test_update_review(self):
        response = self.client.put(f'/api/v1/reviews/{self.review_id}', json={
            "text": "Wonderful stay!",
            "rating": 5
        })
        self.assertEqual(response.status_code, 200)


    def test_get_review_by_place_id(self):
        response = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)


    def test_delete_review(self):
        response = self.client.delete(f'/api/v1/reviews/{self.review_id}')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()