from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import SecurityRecord

class UserAuthTests(TestCase):
    """Test to Verify User oAUTH2.0 Working with simplejwt"""
    def setUp(self):
        """"Create a new user to test"""
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token_url = reverse('token_obtain_pair')


    def test_user_login(self):
        """Test login with the created user in simplejwt"""
        response = self.client.post(self.token_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class SecurityRecordTests(TestCase):
    """test the security record"""
    def setUp(self):
        """create a user and mock security record"""
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }   
        self.user = User.objects.create_user(**self.user_data)
        self.security_record_data = {
            'name': 'Test Security Record',
            'description': 'This is a test security record.',
        }
        
        self.security_record = SecurityRecord.objects.create(**self.security_record_data)
        
        response = self.client.post(self.token_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }, format='json')

        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_security_record(self):
        """Test if can Create a new security record"""
        url = reverse('security-record-list-create')
        data = {
            'name': 'New Security Record',
            'description': 'Description for new security record.',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SecurityRecord.objects.count(), 2)
        self.assertEqual(SecurityRecord.objects.get(id=2).name, 'New Security Record')

    def test_list_security_records(self):
        """Test to retrieve all the security records"""
        url = reverse('security-record-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['security_records']), 1)

    def test_retrieve_security_record(self):
        """Test to retrieve a security records"""
        url = reverse('security-record-detail', args=[self.security_record.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Security Record')

    def test_update_security_record(self):
        """Test to update a security records"""
        url = reverse('security-record-detail', args=[self.security_record.id])
        data = {'name': 'Updated Security Record', 'description': 'Updated description.', 'status': 'inactive'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.security_record.refresh_from_db()
        self.assertEqual(self.security_record.name, 'Updated Security Record')

    def test_delete_security_record(self):
        """Test to delete a security records"""
        url = reverse('security-record-detail', args=[self.security_record.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SecurityRecord.objects.count(), 0)
