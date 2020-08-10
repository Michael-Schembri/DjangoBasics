from django.test import TestCase, Client
from users.models import Profile
from django.contrib.auth.models import User
from datetime import datetime
from pytest import raises

class Test_Views(TestCase):
    
    def setUp(self):
        user = User.objects.filter(username="Profile_user").first()
        if (user):
            self.user = user
        else: 
            self.user = User.objects.create(username="Profile_user", password="testing321")
        self.profile = self.user.profile

    def test_auto_create_profile(self):
        assert self.profile.user == self.user

    def test_cascade_delete_profile(self):
        profile_id = self.profile.id

        self.user.delete()
        with raises(Profile.DoesNotExist):
            profile_retrieved = Profile.objects.get(pk=profile_id)
