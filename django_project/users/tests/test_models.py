from django.test import TestCase, Client
from users.models import Profile
from django.contrib.auth.models import User
from datetime import datetime
from pytest import raises

class Test_Views(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username="Profile_user", password="testing321")
        self.profile = self.user.profile

    def tearDown(self):
        if (self.user.id):
            self.user.delete()

    def test_auto_create_profile(self):
        assert self.profile.user == self.user

    def test_cascade_delete_profile(self):
        profile_id = self.profile.id

        self.user.delete()
        with raises(Profile.DoesNotExist):
            profile_retrieved = Profile.objects.get(pk=profile_id)
