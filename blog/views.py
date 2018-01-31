from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView, CreateView
from django.views.generic.edit import DeleteView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm, NewBoardForm

# Create your views here.

class BoardListView(ListView):
	model = Board
	context_object_name = 'boards'
	template_name = 'home.html'



class TopicListView(ListView):
	model = Topic
	template_name = 'topics.html'
	context_object_name = 'topics'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		kwargs['board'] = self.board
		return super().get_context_data(**kwargs)
	
	def get_queryset(self):
		self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
		queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
		return queryset



class PostListView(ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'topic_posts.html'
	paginate_by = 5

	
	def get_context_data(self, **kwargs):
		
		session_key = 'viewed_topic_{}'.format(self.topic.pk)
		if not self.request.session.get(session_key, False):
			self.topic.views += 1
			self.topic.save()
			self.request.session[session_key] = True

		kwargs['topic'] = self.topic
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
		queryset = self.topic.posts.order_by('created_at')
		return queryset


@method_decorator(login_required, name='dispatch')
class ReplyTopic(CreateView):
	form_class = PostForm
	template_name = 'reply_topic.html'
	context_object_name = 'posts'

	def get_context_data(self, **kwargs):
		self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
		kwargs['topic'] = self.topic
		return super().get_context_data(**kwargs)


	def form_valid(self, form):
		self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
		post = form.save(commit=False)
		post.topic = self.topic
		post.created_by = self.request.user
		post.save()

		self.topic.last_updated = timezone.now()
		self.topic.save()

		topic_url = reverse('topic_posts', kwargs={'pk': self.kwargs.get('pk'), 'topic_pk': self.kwargs.get('topic_pk')})
		topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=self.topic.get_page_count()
            )
		return redirect( topic_post_url )


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):

	model = Post
	fields = ['message', ]
	template_name = 'edit_post.html'
	pk_url_kwarg = 'post_pk'
	context_object_name = 'post'

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(created_by = self.request.user)

	def form_valid(self, form):
		post = form.save(commit=False)
		post.updated_by = self.request.user
		post.updated_at = timezone.now()
		post.save()
		return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk )


@method_decorator(login_required, name='dispatch')
class CreateNewTopic(CreateView):
	form_class = NewTopicForm
	template_name = 'new_topic.html'
	
	def get_context_data(self, **kwargs):
		self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
		kwargs['board'] = self.board
		return super().get_context_data(**kwargs)
	
	def form_valid(self, form):
		self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
		topic = form.save(commit=False)
		topic.board = self.board
		topic.starter = self.request.user
		topic.save()

		post = Post.objects.create(
				message= form.cleaned_data.get('message'),
				topic = topic,
				created_by = self.request.user
			)
		
		return redirect('topic_posts', pk= self.board.pk, topic_pk=topic.pk)
	

class DeleteTopic(DeleteView):
	model = Topic
	success_url = 'board_topics'
	template_name = 'topic_confirm_delete.html'


class CreateNewBoard(CreateView):
	form_class = NewBoardForm
	template_name = 'new_board.html'
	
	def form_valid(self, form):
		board = form.save()
		return redirect('home')



