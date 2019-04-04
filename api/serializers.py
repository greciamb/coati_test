from rest_framework.serializers import ModelSerializer
from api.models import Usuarios

class UsuariosSerializer(ModelSerializer):
	class Meta:
		model = Usuarios
		exclude = ('created_at','updated_at')