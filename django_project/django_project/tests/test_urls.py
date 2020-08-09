from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth import views as auth_views

class Test_Urls(TestCase):
    def test_login_url_resolves(self):
        url = reverse('login')
        assert resolve(url).func.view_class == auth_views.LoginView

    def test_logout_url_resolves(self):
        url = reverse('logout')
        assert resolve(url).func.view_class == auth_views.LogoutView