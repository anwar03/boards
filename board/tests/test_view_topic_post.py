from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase

from ..views import PostListView
from ..models import Board, Topic, Post


class TopicPostViewTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='john', email='john@mail.com', password='1234asdf')
        board = Board.objects.create(name='Django', description='django board.')
        topic = Topic.objects.create(subject='Hello world', board=board, starter=user)
        Post.objects.create(topic=topic, message="i am here.", created_by=user)
        url = reverse('topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

    def test_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEquals(view.func.view_class, PostListView)

