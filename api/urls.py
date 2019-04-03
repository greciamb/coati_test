from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
	#Allows GET, PUT, DELETE
    url(r'^usuario/(?P<pk>[0-9]+)$', views.usuarios_detail),
    #Allows GET, POST
    url(r'^usuarios/$', views.usuarios_list),
    #Allows POST
    url(r'^login/$', views.login),
]

urlpatterns = format_suffix_patterns(urlpatterns)