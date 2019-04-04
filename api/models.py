# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime as times
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from rest_framework_jwt import utils
from rest_framework_jwt.settings import api_settings

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import ugettext as _


class Usuarios(models.Model):
    ROLE = (
        (1,_("Admin")),
        (2,_("User"))
    )
    role = models.IntegerField(choices=ROLE,blank=True,null=True)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=255,blank=True,null=True),
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updated_at', auto_now=True)

    class Meta:
        managed = True
        db_table = 'Usuarios'

    def save(self, *args, **kwargs):
        try:
            if self.id is None:
                self.password =make_password(self.password)
            super(Usuarios, self).save(*args, **kwargs)
        except:
            super(Usuarios, self).save(*args, **kwargs)

    def is_admin(self):
        '''Returns a boolean, True if user is admin, False if not.'''
        return self.role == 1

    def set_password(self,password):
        ''''''
        self.password = make_password(password)
        self.save()

    def check_password(self,password):
        ''''''
        return check_password(password, self.password)

    def create_token(self):
        ''''''
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        api_settings.JWT_EXPIRATION_DELTA = times.timedelta(days=365)
        token = ""
        try:
            user = self
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
        except Exception as e:
            print e
        return token

    def details_dict(self):
        self.token = self.create_token()
        self.save()
        return {'id': self.pk,
                'username': self.username,
                'token': self.token,
                }

    @classmethod
    def get_user_from_token(self, Token):
        ''''''
        userid = -1
        try:
            token = utils.jwt_decode_handler(Token)
            item = Usuarios.objects.get(pk=token['user_id'])            
            if item.username == token['username']:
                userid = token['user_id']
            else:
                userid = -1
        except Exception as e:
            print e

        user = Usuarios.objects.filter(id=userid).first()
        return user

    def __str__(self):
        return self.name