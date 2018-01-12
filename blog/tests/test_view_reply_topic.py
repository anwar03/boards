from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Post, Topic, Board
from ..views import reply_topic

class ReplyTopicTestCase(TestCase):

    def setUp(self):
        self.board = Board.objects.create(name='django', description='django board.')
        self.username = 'john'
        self.password = '1234asdf'
        self.user = User.objects.create_user(username=self.username, email='john@mail.com', password=self.password)
        self.topic = Topic.object.create(subject='test something', board=self.board, starter=self.username)
        Post.object.create(message="this is testing post.", topic=self.topic, created_by=self.user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})


class LoginRiquiredReplyTopicTestCase(TestCase):
    pass


class ReplyTopicTest(TestCase):
    pass 


class SuccessfulReplyTopicTest(TestCase):
    pass 


class InvalidReplyTopicTest(TestCase):
    pass