from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
# Create your views here.

def index(request):
    return render(request, 'index.html')

def guide(request):
    return JsonResponse({1:2})