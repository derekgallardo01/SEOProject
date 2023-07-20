# Create your views here.
from django.shortcuts import render
#from .models import Categories
from categories.models import Category
from exceluser.models import Exceluser
from django.apps import apps
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
import http.client, urllib.request, urllib.parse, urllib.error, base64
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat

import numpy as np


# Create your views here.
