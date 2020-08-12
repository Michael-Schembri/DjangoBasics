from django.test import TestCase
from django.urls import resolve, reverse
from blog.views import about, PostListView

class Test_Urls(TestCase):
    def test_home_url_resolves(self):
        url = reverse('blog-home')
        assert resolve(url).func.view_class == PostListView

    def test_about_url_resolves(self):
        url = reverse('blog-about')
        assert resolve(url).func == about