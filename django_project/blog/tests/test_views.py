from django.test import TestCase, Client
from blog.views import home, about
from django.urls import reverse
from blog.models import Post
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth.models import User

import json

class Test_Views(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('blog-home')
        self.about_url = reverse('blog-about')
        self.user = User.objects.create(username="posts_user", password="testing321")
        self.post = Post.objects.create(title='Test post', content='test post content', author=self.user)
        self.post_count = Post.objects.count()

    def test_home_GET(self):
        response = self.client.get(self.home_url)

        assert response.context['posts'].count() == self.post_count
        assert response.status_code == 200
        assertTemplateUsed(response, 'blog/home.html')
    
    def test_about_GET(self):
        response = self.client.get(self.about_url)
        
        assert response.status_code == 200
        assertTemplateUsed(response, 'blog/about.html')