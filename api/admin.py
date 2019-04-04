# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Usuarios

import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib import auth

# Register your models here.

class UsuariosAdmin(admin.ModelAdmin):
	list_display = ('username','password')


admin.site.register(Usuarios,UsuariosAdmin)