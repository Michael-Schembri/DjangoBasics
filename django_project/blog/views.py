from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('<H1>Blog Home</H1>')

def about(request):
    return HttpResponse('<H1>Blog About</H1>')

