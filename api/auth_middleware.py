# -*- coding: utf-8 -*-
from django.http import JsonResponse
from api.models import Usuarios


class AuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.usuario = get_usuario_from_request(request)

        return self.get_response(request)


def get_admin_request(request):
    """Returns the user associated with a request or None.
    Obtains the user from the token that comes in the HTTP header
    "AUTHORIZATION"
    """
    token = request.META.get("HTTP_AUTHORIZATION", "")
    return Usuario.get_user_from_token(token)


def login_required(func):
    """Decorator that makes sure that there is a user logged in to the
    system. Otherwise returns a json message with a 401 status_code"""

    def wrapped_func(request, *args, **kwargs):
        if request.usuario is None:
            response = {'success': False,
                        'errors': ["Se necesita iniciar sesion " +
                                   "para usar este metodo"],
                        'status': 401}
            return JsonResponse(response, status=401, safe=False)
        else:
            return func(request, *args, **kwargs)

    # return the actual function
    return wrapped_func


def is_admin(func):
    """Decorator that makes sure that there is a user logged in to the
    system. Otherwise returns a json message with a 401 status_code"""

    def wrapped_func(request, *args, **kwargs):
        if request.usuario is None:
            response = {'success': False,
                        'errors': ["Se necesita iniciar sesion para usar este metodo"],
                        'status': 401}
            return JsonResponse(response, status=401, safe=False)
        else:
            if request.usuario.is_admin():
                return func(request, *args, **kwargs)
            else: 
                response = {'success': False,
                        'errors': ["No se tiene permisos para usar este método"],
                        'status': 401}
                return JsonResponse(response, status=401, safe=False)

    # return the actual function
    return wrapped_func