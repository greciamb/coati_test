# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Usuarios
from api.serializers import UsuariosSerializer
from django.http import JsonResponse

from django.shortcuts import render

# Create your views here.
url = "http://localhost:8000"

@api_view(['GET','PUT','POST','DELETE'])
def usuarios_detail(request,pk):
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		pass
	elif request.method == 'DELETE':
		pass

@api_view(['GET','POST'])
def usuarios_list(request):
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		pass

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        pass