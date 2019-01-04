# from django import forms
# from django.forms.utils import ErrorList
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin

# Create your views here.

class TweetCreateView(FormUserNeededMixin,CreateView):
# class TweetCreateView(LoginRequiredMixin,FormUserNeededMixin,CreateView):
	#queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = 'tweets/create_view.html'
	#fields = ['user','content']
	# success_url = '/tweet/create/'	
	# login_url = '/admin/'


	# def form_valid(self, form):
 #    	# This method is called when valid form data has been POSTed.
 #    # It should return an HttpResponse.
	#     #form.send_email()
	# 	if self.request.user.is_authenticated():
	# 		form.instance.user = self.request.user
	# 		return super(TweetCreateView, self).form_valid(form)
	# 	else:
	# 		form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must  be logged in to continue"])
	# 		return self.form_invalid(form)

class TweetUpdateView(LoginRequiredMixin,UserOwnerMixin,UpdateView):
	queryset = Tweet.objects.all() 
	form_class = TweetModelForm
	template_name = 'tweets/update_view.html'
	# success_url = '/tweet/'

class TweetDeleteView(LoginRequiredMixin,DeleteView):
	model = Tweet
	template_name = 'tweets/delete_confirm.html'
	success_url = reverse_lazy("tweet:list")

class TweetDetailView(DetailView):
	queryset = Tweet.objects.all()
	#template_name = 'tweets/detail_view.html'

	# def get_object(self,):
	# 	return Tweet.objects.get(id = 1)

class TweetListView(ListView):
	#template_name = 'tweets/list_view.html'

	def get_queryset(self,*args,**kwargs):
		qs = Tweet.objects.all()
		print('qs_first: ',qs)
		print(self.request.GET)
		query = self.request.GET.get("q",None)
		print('query: ',query)
		if query is not None:
			qs = qs.filter(
				# content__icontains=query
				# user__username__icontains=query,
				Q(content__icontains=query)|
				Q(user__username__icontains=query)
				)
		print('qs:',qs)
		return qs

	def get_context_data(self,*args,**kwargs):
		context = super(TweetListView, self).get_context_data(*args, **kwargs)
		return context





def tweet_detail_view(request,id = 1):
	obj = Tweet.objects.get(id = id )
	context = { "object" : obj,'abc':obj}
	print(obj)

	return render(request,"tweets/detail_view.html",context)

def tweet_list_view(request):
	queryset = Tweet.objects.all()
	print(queryset)
	for obj in queryset:
		print(obj.content)
	context = { "object_list" : queryset}
	return render(request,"tweets/list_view.html",context)