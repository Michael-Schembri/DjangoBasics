from django.test import TestCase, Client
from django.contrib.auth.models import User
from users.views import profile, register
from django.urls import reverse
from users.models import Profile 
from pytest_django.asserts import assertTemplateUsed, assertRedirects
import json
import pytest

class Test_Views(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.profile_url = reverse("profile")
        cls.register_url = reverse("register")
        cls.login_url = reverse("login") 
    
    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.user = User.objects.create(username="Profile_user", email='profileUser@company.com')
        self.user.set_password('testing321')
        self.user.save()

    def tearDown(self):
        self.client.logout()
        self.user.delete()


    def test_register_GET(self):
        response = self.client.get(self.register_url)
        
        assert response.status_code == 200
        assertTemplateUsed(response, "users/register.html")
    
    def test_register_POST(self):
        cred = {
            "username": "testuser",
            "email": "test@company.com",
            "password1": "testing321",
            "password2": "testing321"}

        response = self.client.post(self.register_url,cred)

        created_user = User.objects.filter(username=cred["username"]).first()
        assert created_user.username == cred["username"]
        
        self.assertRedirects(response, self.login_url, status_code=302, 
        target_status_code=200, fetch_redirect_response=True)
        
    def test_register_POST_invalid(self):
            cred = {
            "username": "test_bad",
            "email": "test_bad",
            "password1": "testing321",
            "password2": "testing321"}

            response = self.client.post(self.register_url,cred) 
            
            created_user = User.objects.filter(username=cred["username"]).first()
            assert created_user == None

    def test_profile_GET_not_logged_in(self):
        response = self.client.get(self.profile_url, follow=True)
        self.assertRedirects(response, self.login_url+"?next="+self.profile_url, status_code=302, 
        target_status_code=200, fetch_redirect_response=True)

    def test_profile_GET_logged_in(self):
        logged_in = self.client.login(username = self.user.username, password='testing321')
        assert logged_in == True
        
        response = self.client.get(self.profile_url, follow=True) 
        
        assert response.status_code == 200
        assertTemplateUsed(response, "users/profile.html")

    def test_profile_POST_change_email(self):
        logged_in = self.client.login(username = self.user.username, password='testing321')
        assert logged_in == True
        data = {
            "username": self.user.username,
            "email": 'updated_email@company.com'}

        response = self.client.post(self.profile_url, data) 
        
        updated_user = User.objects.filter(username=data["username"]).first()
        assert updated_user.email == data['email']

    def test_profile_POST_change_email_invalid(self):
        logged_in = self.client.login(username = self.user.username, password='testing321')
        assert logged_in == True
        data = {
            "username": self.user.username,
            "email": 'updated_email'}

        response = self.client.post(self.profile_url, data) 
        updated_user = User.objects.filter(username=data["username"]).first()

        assert updated_user.email != data['email']
        assert updated_user.email == self.user.email
 
        