from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from companies.models import Company


class CompanyModelTest(TestCase):
    def setUp(self):
        self.company_data = {
            "id": "COMP001",
            "name": "Test Company",
            "email": "test@company.com",
            "phone": "+1234567890",
            "address": "Test Address",
        }
        self.company = Company.objects.create(**self.company_data)

    def test_company_creation(self):
        """Test company creation with required fields"""
        self.assertEqual(self.company.id, self.company_data["id"])
        self.assertEqual(self.company.name, self.company_data["name"])
        self.assertEqual(self.company.email, self.company_data["email"])
        self.assertEqual(self.company.phone, self.company_data["phone"])
        self.assertEqual(self.company.address, self.company_data["address"])

    def test_company_creation_without_optional_fields(self):
        """Test company creation without optional fields"""
        company_data = {
            "id": "COMP002",
            "name": "Test Company 2",
            "email": "test2@company.com",
            "phone": "",
        }
        company = Company.objects.create(**company_data)
        self.assertEqual(company.id, company_data["id"])
        self.assertEqual(company.name, company_data["name"])
        self.assertEqual(company.email, company_data["email"])
        self.assertEqual(company.phone, "")
        self.assertIsNone(company.address)

    def test_company_unique_constraints(self):
        """Test unique constraints for company id and email"""
        # Test duplicate company id
        with self.assertRaises(Exception):
            Company.objects.create(**self.company_data)

        # Test duplicate email
        duplicate_email_data = {
            "id": "COMP003",
            "name": "Test Company 3",
            "email": "test@company.com",
            "phone": "+1234567890",
        }
        with self.assertRaises(Exception):
            Company.objects.create(**duplicate_email_data)


class CompanyAPITest(APITestCase):
    def setUp(self):
        self.company_data = {
            "id": "COMP001",
            "name": "Test Company",
            "email": "test@company.com",
            "phone": "+1234567890",
            "address": "Test Address",
        }
        self.company = Company.objects.create(**self.company_data)
        self.url = reverse("companies:company-list")

    def test_list_companies(self):
        """Test GET request to list all companies"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.company.id)

    def test_create_company(self):
        """Test POST request to create a new company"""
        new_company_data = {
            "id": "COMP002",
            "name": "New Company",
            "email": "new@company.com",
            "phone": "+1987654321",
            "address": "New Address",
        }
        response = self.client.post(self.url, new_company_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)
        self.assertEqual(Company.objects.get(id="COMP002").name, "New Company")

    def test_create_company_without_optional_fields(self):
        """Test POST request to create a company without optional fields"""
        new_company_data = {
            "id": "COMP002",
            "name": "New Company",
            "email": "new@company.com",
            "phone": "",
        }
        response = self.client.post(self.url, new_company_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)
        company = Company.objects.get(id="COMP002")
        self.assertEqual(company.phone, "")

    def test_create_company_validation(self):
        """Test validation when creating a company with invalid data"""
        # Test duplicate company id
        response = self.client.post(self.url, self.company_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test duplicate email
        duplicate_email_data = {
            "id": "COMP003",
            "name": "Test Company 3",
            "email": "test@company.com",
            "phone": "+1234567890",
        }
        response = self.client.post(
            self.url, duplicate_email_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_company(self):
        """Test GET request to retrieve a single company"""
        url = reverse("companies:company-detail", kwargs={"pk": self.company.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.company.id)

    def test_update_company(self):
        """Test PUT request to update a company"""
        url = reverse("companies:company-detail", kwargs={"pk": self.company.id})
        updated_data = {
            "id": "COMP001",
            "name": "Updated Company",
            "email": "test@company.com",
            "phone": "+1234567890",
            "address": "Updated Address",
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, "Updated Company")
        self.assertEqual(self.company.address, "Updated Address")

    def test_partial_update_company(self):
        """Test PATCH request to partially update a company"""
        url = reverse("companies:company-detail", kwargs={"pk": self.company.id})
        partial_data = {"name": "Updated Company"}
        response = self.client.patch(url, partial_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, "Updated Company")

    def test_delete_company(self):
        """Test DELETE request to delete a company"""
        url = reverse("companies:company-detail", kwargs={"pk": self.company.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)


class CompanyWithUsersTest(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username="user1", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="testpass123"
        )
        self.user3 = User.objects.create_user(
            username="user3", password="testpass123"
        )

        # Create company with users
        self.company_data = {
            "id": "COMP001",
            "name": "Test Company",
            "email": "test@company.com",
            "phone": "+1234567890",
            "address": "Test Address",
            "user1": self.user1,
            "user2": self.user2,
            "user3": self.user3,
        }
        self.company = Company.objects.create(**self.company_data)
        self.url = reverse("companies:company-list")

    def test_company_with_users(self):
        """Test company creation and retrieval with associated users"""
        # Test company creation with users
        new_company_data = {
            "id": "COMP002",
            "name": "New Company",
            "email": "new@company.com",
            "phone": "+1987654321",
            "user1": self.user1.id,
            "user2": self.user2.id,
        }
        response = self.client.post(self.url, new_company_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify users are associated
        company = Company.objects.get(id="COMP002")
        self.assertEqual(company.user1, self.user1)
        self.assertEqual(company.user2, self.user2)
        self.assertIsNone(company.user3)

    def test_update_company_users(self):
        """Test updating company's associated users"""
        url = reverse("companies:company-detail", kwargs={"pk": self.company.id})
        updated_data = {
            "id": "COMP001",
            "name": "Test Company",
            "email": "test@company.com",
            "phone": "+1234567890",
            "address": "Test Address",
            "user1": self.user2.id,
            "user2": self.user1.id,
            "user3": self.user3.id,
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.user1, self.user2)
        self.assertEqual(self.company.user2, self.user1)
        self.assertEqual(self.company.user3, self.user3)
