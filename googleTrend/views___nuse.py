from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect

def special_admin_page(request):
    return HttpResponse('ddd')