from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import ModelForm

from ..models import Board, Post, Topic
from ..views import PostUpdateView


class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django boards.')
        self.username = 'john'
        self.password = '1234asdf'
        self.user = User.objects.create_user(username=self.username, email='shorif@gmail.com', password=self.password)
        self.topic = Topic.objects.create(subject='test django', board = self.board, starter=self.user)
        self.post = Post.objects.create(message = 'test first post', topic=self.topic, created_by=self.user)
        self.url = reverse('edit_post', kwargs={
            'pk': self.post.topic.board.pk, 'topic_pk': self.post.topic.pk, 'post_pk': self.post.pk
        })


class LoginRequiredPostUpdateViewTestCase(PostUpdateViewTestCase):
    
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url = login_url, url=self.url))


class UnauthorizedPostUpdateViewTestCase(PostUpdateViewTestCase):

    def setUp(self):

        super().setUp()

        username = 'jan'
        password = '1234'
        user = User.objects.create_user(username=username, email='bang@mail.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)
        
    
    def test_status_code(self):
        self.assertEqual(self.response.status_code, 404)
    

class PostUpdateViewTests(PostUpdateViewTestCase):
    
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/boards/1/topics/1/post/1/edit/')
        self.assertEquals(view.func.view_class, PostUpdateView)
    
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)
    
    def test_input_forms(self):
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)
    

class SuccessfulPostUpdateViewTests(PostUpdateViewTestCase):
    
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': 'edited message.'})
    
    def test_redirection(self):
        topic_posts_url = reverse('topic_posts', kwargs={ 'pk': self.board.pk, 'topic_pk': self.topic.pk })
        self.assertRedirects(self.response, topic_posts_url )

    def test_post_changed(self):
        self.post.refresh_from_db()
        self.assertEquals(self.post.message, 'edited message.')

class InvalidPostUpdateViewTests(PostUpdateViewTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)