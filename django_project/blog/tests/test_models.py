from django.test import TestCase, Client
from blog.models import Post
from django.contrib.auth.models import User
from datetime import datetime
from pytest import raises

class Test_Views(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username="posts_user", password="testing321")
        self.sample_post = self.user.post_set.create(title = 'sample', content = 'sample content')

    def tearDown(self):
        if self.user.id:
            self.user.delete()

    def test_auto_assigned_date_on_post(self):
        post = self.user.post_set.create(title='Test post', content='test post content')
        dt = datetime.utcnow()

        compare_date = datetime(dt.year, dt.month, dt.day)
        post_date = datetime(post.date_posted.year, post.date_posted.month, post.date_posted.day)

        assert post_date == compare_date
        
    def test_cascade_delete_post(self):
        post_id = self.sample_post.id
        
        self.user.delete()
        with raises(Post.DoesNotExist):
            post_retrieved = Post.objects.get(pk=post_id)
