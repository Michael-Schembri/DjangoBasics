from django.test import TestCase, Client
from blog.views import about, PostListView, PostDetailView, PostCreateView
from django.urls import reverse
from blog.models import Post
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth.models import User

class Test_Views(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.home_url = reverse('blog-home')
        cls.about_url = reverse('blog-about')
        cls.login_url = reverse("login") 
        cls.create_url = reverse('post-create')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.user = User.objects.create(username="Profile_user", email='profileUser@company.com')
        self.user.set_password('testing321')
        self.user.save()

        self.post = self.user.post_set.create(title='Test post', content='test post content')
        self.post = self.user.post_set.create(title='Test post1', content='test post content')
        self.post = self.user.post_set.create(title='Test post2', content='test post content')
        self.post = self.user.post_set.create(title='Test post3', content='test post content')

        self.detail_url = reverse('post-detail',  args=[self.post.id])
        self.post_count = Post.objects.count()
        self.posts_per_page = PostListView.paginate_by

    def tearDown(self):
        self.user.delete()

    def test_home_GET(self):
        response = self.client.get(self.home_url)
 
        assert response.context['posts'].count() == min(self.post_count, self.posts_per_page)
        assert response.status_code == 200
        assertTemplateUsed(response, 'blog/home.html')
    
    def test_about_GET(self):
        response = self.client.get(self.about_url)
        
        assert response.status_code == 200
        assertTemplateUsed(response, 'blog/about.html')

    
    def test_post_detail_GET(self):
        response = self.client.get(self.detail_url)

        post = response.context['post']
        assert post.id == self.post.id
        assert post.title == self.post.title
        assert response.status_code == 200
        assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_create_GET_not_logged_in(self):
        response = self.client.get(self.create_url)

        self.assertRedirects(response, self.login_url+"?next="+self.create_url, status_code=302, 
        target_status_code=200, fetch_redirect_response=True)

    def test_post_create_GET_logged_in(self):
        logged_in = self.client.login(username = self.user.username, password='testing321')
        assert logged_in == True
        
        response = self.client.get(self.create_url) 
        
        assert response.status_code == 200