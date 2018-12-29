from django.shortcuts import render
from .models import Tweet
# Create your views here.
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