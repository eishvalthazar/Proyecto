from rest_framework import status
from rest_framework.views import (
    APIView,
    Response
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from config.pagination import Paginacion
from .models import (
    Usuario,
)
from .serializers import (
    UsuarioListRetrieveSerializer,
    UsuarioCreateUpdateSerializer,
    PerfilSerializer,
)
from config.mixins import ProtectedForeignKeyDeleteMixin
from apps.seguridad.permissions import EsUsuarioAdministrador


class UsuarioListCreateAPIView(ListCreateAPIView):
    """
    Se encarga de listar y crear los usuarios, soporta los métodos:
    GET y POST
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioListRetrieveSerializer
    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username')
    pagination_class = Paginacion

    def get_serializer_class(self):
        if self.request and self.request.method == 'POST':
            return UsuarioCreateUpdateSerializer
        return UsuarioListRetrieveSerializer

    def get_queryset(self):
        return Usuario.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class UsuarioRetrieveUpdateDestroyAPIView(ProtectedForeignKeyDeleteMixin, RetrieveUpdateDestroyAPIView):
    """
    Se encarga de visualizar, editar y borrar los usuarios, soporta los métodos:
    GET, PUT y DELETE
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioListRetrieveSerializer
    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request and self.request.method == 'PUT':
            return UsuarioCreateUpdateSerializer
        return UsuarioListRetrieveSerializer

    def get_queryset(self):
        return Usuario.objects.all()


class RolesUsuarioListAPIView(APIView):
    """
    Se encarga de listar los roles de usuario
    """

    def get(self, request):
        lista_elementos = []

        for elemento in Usuario.ROLES:
            lista_elementos.append({
                'codigo': elemento[0],
                'descripcion': elemento[1],
            })
        return Response(lista_elementos, status=status.HTTP_200_OK)


class PerfilView(APIView):
    """
    Se encarga de actualizar el perfil de usuario, soporta los métodos:
    GET y PUT
    """

    def get(self, request):
        serializer = PerfilSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = PerfilSerializer(request.user, data=request.data)
        nuevo_password = request.data.get('nuevo_password', None)
        actual_password = request.data.get('actual_password', None)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'detail': 'Petición no válida.', 'errores': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        if nuevo_password:
            if request.user.check_password(actual_password):
                try:
                    request.user.set_password(nuevo_password)
                    request.user.save()
                except Exception:
                    return Response({"detail": "Error al actualizar el password."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"detail": "Las contraseñas no coinciden."},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Perfil actualizado correctamente.."},
                        status=status.HTTP_200_OK)


class UsuarioGenerarClaveAPIView(APIView):
    """
    Se encarga de generar una nueva clave al usuario y enviarla por correo
    soporta el método GET
    """
    permission_classes = (IsAuthenticated, EsUsuarioAdministrador)

    def get(self, request, uuid):
        try:
            kwargs = {'uuid': uuid}
            if not request.user.is_staff:
                kwargs['cliente'] = request.user.cliente

            usuario = Usuario.objects.get(**kwargs)
        except Usuario.DoesNotExist:
            usuario = None

        usuario.generar_nueva_clave()

        return Response({'detail': 'Clave de usuario generada correctamente.'})
