import polls.youtubechat
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    dict = polls.youtubechat.main()
    return render(request, 'index.html', dict)
