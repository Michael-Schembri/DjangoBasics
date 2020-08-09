from django.test import TestCase, Client
from django.contrib.auth.models import User
from users.views import profile, register
from django.urls import reverse
from users.models import Profile 
from pytest_django.asserts import assertTemplateUsed, assertRedirects
import json
import pytest

class Test_Views(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile_url = reverse("profile")
        self.register_url = reverse("register")
        self.login_url = reverse("login") 

    def test_profile_GET_not_logged_in(self):
        response = self.client.get(self.profile_url, follow=True)
        self.assertRedirects(response, self.login_url+"?next="+self.profile_url, status_code=302, 
        target_status_code=200, fetch_redirect_response=True)

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
        
    # @pytest.mark.parametrize("user,email,password1,password2,expects", argvalues =[
    #     ("test_bad", "test_bad@company.com", "testing321", "testing321", "test"),
    #     ("test_bad", "test_bad@company.com", "testing321", "testing321", "test"), #duplicate
    #     ("test_bad", "test_bad", "testing321", "testing321", "test"), #bad email
    #     ("test_bad", "test_bad@company.com", "testing", "testing321", "test"),  #mismatched password
    # ])
    def test_register_POST_invalid(self):
            cred = {
            "username": "test_bad",
            "email": "test_bad",
            "password1": "testing321",
            "password2": "testing321"}

            response = self.client.post(self.register_url,cred) 
            
            created_user = User.objects.filter(username=cred["username"]).first()
            assert created_user == None

 
        