from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import dns.resolver

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Usuários devem ter um endereço de email válido')
        
        email = self.normalize_email(email)
        checkDns(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
        validators=[EmailValidator()]
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        # Validação de DNS
        checkDns(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin
def checkDns(email):
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
    except dns.resolver.NoAnswer:
        raise ValidationError(f'O domínio {domain} não possui registros MX válidos.')
    except dns.resolver.NXDOMAIN:
        raise ValidationError(f'O domínio {domain} não existe.')
    except dns.resolver.LifetimeTimeout:
        raise ValidationError("Não foi possível contactar o DNS.")
    except Exception as e:
        raise ValidationError(f'Erro desconhecido ao verificar o DNS: {e}')


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    stat = models.CharField(max_length=10, choices=[('pendente', 'Pendente'), ('concluida', 'Concluída')], default='pendente')
    datacriacao = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.titulo

class DemoModel(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to="demo_images")

    def __str__(self):
        return self.title
