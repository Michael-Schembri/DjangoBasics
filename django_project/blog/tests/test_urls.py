from django.test import TestCase
from django.urls import resolve, reverse
from blog.views import about, PostListView, PostDetailView, PostCreateView, PostUpdateView

class Test_Urls(TestCase):
    def test_home_url_resolves(self):
        url = reverse('blog-home')
        assert resolve(url).func.view_class == PostListView

    def test_post_detail_url_resolves(self):
        url = reverse('post-detail',args=[1])
        assert resolve(url).func.view_class == PostDetailView

    def test_post_create_url_resolves(self):
        url = reverse('post-create')
        assert resolve(url).func.view_class == PostCreateView

    def test_post_create_url_resolves(self):
        url = reverse('post-create', args=[1])
        assert resolve(url).func.view_class == PostCreateView

    def test_about_url_resolves(self):
        url = reverse('blog-about')
        assert resolve(url).func == about