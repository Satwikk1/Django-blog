from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Posts
from django.views.generic import (
					ListView, 
					DetailView, 
					CreateView,
					UpdateView,
					DeleteView
			)
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def home(request):        # same as the class based view which is the class next to this function. class based views are more convienent to user.
	context={
		'posts': Posts.objects.all()
	}
	return render(request, 'blog/home.html', context)

class PostListView(LoginRequiredMixin, ListView):
	model=Posts
	template_name='blog/home.html'
	context_object_name='posts'
	paginate_by=5

class UserPostListView(LoginRequiredMixin, ListView):   # admin listView filter
	model=Posts
	template_name='blog/user_posts.html'
	context_object_name='posts'
	ordering=['-date_posted']
	paginate_by=5

	def get_queryset(self):
		user=get_object_or_404(User, username=self.kwargs.get('username'))
		return Posts.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(LoginRequiredMixin, DetailView):
	model=Posts

class PostCreateView(LoginRequiredMixin, CreateView):
	model=Posts
	fields=['title', 'content']

	def form_valid(self, form):
		form.instance.author=self.request.user
		return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model=Posts
	fields=['title', 'content']

	def form_valid(self, form):
		form.instance.author=self.request.user
		return super().form_valid(form)

	def test_func(self):
		post=self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model=Posts
	success_url='/'

	def test_func(self):
		post=self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False



@login_required
def about(request):
    return render(request, 'blog/about.html')

