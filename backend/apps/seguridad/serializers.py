from rest_framework import serializers

from .models import Usuario


class UsuarioListRetrieveSerializer(serializers.ModelSerializer):
    rol = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ['uuid', 'username', 'first_name', 'last_name', 'email', 'rol']

    def get_rol(self, obj):
        return {
            'codigo': obj.rol,
            'descripcion': obj.get_rol_display()
        }


class UsuarioCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['uuid', 'username', 'first_name', 'last_name', 'email', 'rol']


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['uuid', 'first_name', 'last_name', 'email']
