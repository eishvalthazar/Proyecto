import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

from model_utils.models import TimeStampedModel
from .managers import UsuarioManager
from .utils import generar_cadena_aleatoria


class Usuario(AbstractUser, TimeStampedModel):
    """
    Representa un Usuario en el sistema
    """
    ROL_ADMINISTRADOR = 'AD'
    ROLES = (
        (ROL_ADMINISTRADOR, 'Administrador'),
    )
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    rol = models.CharField(
        choices=ROLES,
        max_length=2,
        verbose_name='rol'
    )

    email = models.EmailField(unique=True)

    objects = UsuarioManager()

    class Meta:
        app_label = 'seguridad'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        default_permissions = ()

    def __str__(self):
        """
        Retorna la representación de la instancia del modelo
        """
        return self.email

    def save(self, *args, **kwargs):
        creando = not self.pk
        super(Usuario, self).save(*args, **kwargs)

        if creando:
            self.generar_nueva_clave()

    def generar_nueva_clave(self):
        password = generar_cadena_aleatoria(6)
        self.set_password(password)
        self.save()
        self.enviar_datos_acceso(password)

    def enviar_datos_acceso(self, password):
        asunto = 'CYA TEMPORALES - Datos de acceso'
        datos = {
            'nombre_completo': self.get_full_name(),
            'username': self.username,
            'contraseña': password,
            'site_url': settings.SITE_URL
        }

        mensaje = render_to_string('emails/generar_contrasena.html', {'datos': datos})
        self.enviar_mail(asunto, mensaje)

    def enviar_mail(self, asunto, mensaje):
        send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [self.email], html_message=mensaje,
                  fail_silently=False)
