from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from vinyl.models import Record


class RecordAPITest(APITestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.list_url = "/api/v1/records/"
        self.detail_url = "/api/v1/records/1/"
        self.not_found_url = "/api/v1/records/9999/"

        self.regular_user = User.objects.create_user(
            username="regular_user",
            email="user@example.com",
            password="UserPassword"
        )

        self.admin_user = User.objects.create_superuser(
            username="admin_user",
            email="admin@example.com",
            password="AdminPassword"
        )

        self.valid_payload = {
            "title": "Abbey Road",
            "artist": 1,
            "label": 1,
            "genres": [1],
            "release_year": 1969,
            "price": "1550.00",
            "stock_quantity": 6,
            "description": "Класичний альбом."
        }

    def test_get_records_list_as_guest(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_get_record_detail_as_guest(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "The Dark Side of the Moon")

    def test_create_record_unauthenticated_fails(self):
        response = self.client.post(self.list_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_record_as_authenticated_succeds(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(self.list_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Record.objects.count(), 6)
        self.assertEqual(response.data["title"], "Abbey Road")

    def test_create_record_invalid_data_fails(self):
        self.client.force_authenticate(user=self.regular_user)
        invalid_payload = {
            "title": "",
            "artist": 9999,
            "label": 1,
            "genres": [],
            "release_year": 1800,
            "price": "-100.00"
        }
        response = self.client.post(self.list_url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_record_as_regular_user_forbidden(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.put(self.detail_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_record_as_admin_succeds(self):
        self.client.force_authenticate(user=self.admin_user)
        updated_data = self.valid_payload.copy()
        updated_data["title"] = "The Dark Side of the Moon (Remastered)"

        response = self.client.put(self.detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "The Dark Side of the Moon (Remastered)")

    def test_delete_record_as_regular_user_forbidden(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_record_as_admin_succeeds(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Record.objects.filter(pk=1).exists())

    def test_delete_nonexistent_record_404(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.not_found_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        