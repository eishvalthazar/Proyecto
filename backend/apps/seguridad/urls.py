from rest_framework_jwt.views import obtain_jwt_token

from django.urls import path

from .views import (
    UsuarioListCreateAPIView,
    UsuarioRetrieveUpdateDestroyAPIView,
    RolesUsuarioListAPIView,
    PerfilView,
    UsuarioGenerarClaveAPIView,
)

urlpatterns = [
    path('login/', obtain_jwt_token, name='seguridad-login-api'),
    path('usuarios/', UsuarioListCreateAPIView.as_view(), name='seguridad-usuarios-api'),
    path('usuarios/<uuid:uuid>/', UsuarioRetrieveUpdateDestroyAPIView.as_view(), name='seguridad-usuarios-api'),
    path('usuarios/roles/', RolesUsuarioListAPIView.as_view(), name='seguridad-usuarios-roles-api'),
    path('usuarios/generar_clave/<uuid:uuid>/', UsuarioGenerarClaveAPIView.as_view(),
         name='seguridad-usuarios-generar-clave'),
    path('perfil/', PerfilView.as_view(), name='seguridad-perfil'),
]
