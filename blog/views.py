from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import post
from django.contrib.auth.decorators import login_required
from django.views.generic import (
			ListView,
			DetailView,
			CreateView,
			UpdateView,
			DeleteView
			)
# Create your views here.
#create  a list here
@login_required
def home(request):
	context={
	'Posts':post.objects.all()
	}
	return render(request,'blog/Home.html',context)

class PostListView(ListView):
	model=post
	template_name='blog/Home.html'
	context_object_name='Posts'
	paginate_by=7



class UserPostListView(ListView):
	model=post
	template_name='blog/user_posts.html'
	context_object_name='Posts'
	paginate_by=10

	def get_queryset(self):
		user=get_object_or_404(User,username=self.kwargs.get('username'))
		return post.objects.filter(author=user).order_by('-posted_date')

class PostDetailView(DetailView):
	model=post



class PostCreateView(LoginRequiredMixin,CreateView):
	model=post
	fields=['title','content']

	def form_valid(self,form):
		form.instance.author=self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model=post
	fields=['title','content']

	def form_valid(self,form):
		form.instance.author=self.request.user
		return super().form_valid(form)
	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model=post
	success_url='/blog/'
	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False

@login_required
def about(request):
	context={
	'posts':post
	}
	return render(request,'blog/About.html',context,{'title':'About'})
