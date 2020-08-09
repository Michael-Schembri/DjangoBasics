from django.test import TestCase
from django.urls import resolve, reverse
from users.views import register, profile

class Test_Urls(TestCase):
    def test_register_url_resolves(self):
        url = reverse('register')
        assert resolve(url).func == register

    def test_profile_url_resolves(self):
        url = reverse('profile')
        assert resolve(url).func == profile