# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from api.auth_middleware import login_required,is_admin
from rest_framework.response import Response
from api.models import Usuarios
from api.serializers import UsuariosSerializer
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password

from django.shortcuts import render

# Create your views here.
url = "http://localhost:8000"

def check_errors_password(password):
    """Revisa las condiciones de una buena contraseña y devuelve una
    lista de errores."""
    errors = []
    if len(password) < 6:
        errors.append("La contraseña debe tener al menos 6 caracteres")
    return errors


def check_errors_create_account(username, password):
    errors = []
    username_query = Usuarios.objects.filter(username=username)

    if not username and (username_query.count() >= 1):
        errors.append("Ese usuario ya está vinculado a otra cuenta")

    errors.extend(check_errors_password(password))

    return errors


def check_errors_login(username, password):
    errors = []

    if not username:
        errors.append("No se especifico el nombre de usuario")

    if not password:
        errors.append(u"No se especifico la contraseña")

    return errors

@login_required
@api_view(['GET','PUT','DELETE'])
def usuarios_detail(request,pk):
    try:
        item = Usuarios.objects.get(pk=pk)
    except Usuarios.DoesNotExist:
        return Response({'status': False, 'errors': ['El usuario no existe', ]}, status=400)

    if request.method == 'GET':
        serializer = UsuariosSerializer(item)
        return Response({'status': True, 'data': serializer.data})

    else:
        return edit_usuario(request, item)


@is_admin
def edit_usuario(request, item):
    if request.method == 'PUT':
    	request.POST._mutable =True
    	request.data['password']=make_password(request.data.get('password',''))
    	serializer = UsuariosSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({'status': True, 'data': serializer.data})
        return Response({'status': False, 'data': serializer.errors}, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@login_required
@api_view(['GET','POST'])
def usuarios_list(request):
    if request.method == 'GET':
        items = Usuarios.objects.all()
        serializer = UsuariosSerializer(items, many=True)
        return Response({'success': True, 'data': serializer.data})

    else:
        return create_usuario(request)


@is_admin
def create_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        role = request.POST.get('role', '')
        errors = check_errors_create_account(username, password)

        status = 400
        response = {'success': (len(errors) == 0),
                    'errors': errors}

        if response['success']:
            # successs
            status = 200
            new_user = Usuarios(username=username, role=role,password=password)
            new_user.save()
            # new_user.set_password(password)
            response['data'] = new_user.details_dict()
        else:
            logger.error(errors)

            # We return the response
            # We need to use unsafe mode to return a list of errors
        return JsonResponse(response, safe=False, status=status, content_type='application/json')

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        errors = check_errors_login(username, password)
        user = Usuarios.objects.get(username=username)
        status = 200
        # check that that the account exists
        if (not errors) and (user is None):
            # username does not exist
            errors.append("Usuario no encontrado")

        # check password matches
        if not errors:

            if not user.check_password(password):
                errors.append("Contraseña incorrecta")

        # check that the email has been confirmed
        #    if not errors and user.email == "":
        #        errors.append("Se necesita confirmar el email" +
        #                      " de la cuenta para iniciar sesión")
        if not errors:
            # Success
            response = {'success': True,
                        'data': user.details_dict()}
        else:
            # Error
            status = 400
            response = {'success': False,
                        'errors': errors}

        return JsonResponse(response, safe=False, status=status)
    return None