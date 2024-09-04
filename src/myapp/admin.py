from django.contrib import admin
from .models import User, Task  # Adicionando User e Task
from .forms import UserCreationForm, TaskForm  # Adicionando forms para Task e User



# Configurando o admin para User
class UserAdmin(admin.ModelAdmin):
    form = UserCreationForm
    list_display = ('email', 'is_active', 'is_staff')  # Campos que serão exibidos no admin
    search_fields = ('email',)  # Campos de busca

class TaskAdmin(admin.ModelAdmin):
    form = TaskForm
    list_display = ('titulo', 'descricao', 'get_status', 'user', 'get_created_at')  # Atualizando campos
    search_fields = ('titulo', 'descricao')  # Campos de busca

    # Métodos para exibir os valores corretos no admin
    def get_status(self, obj):
        return obj.status
    get_status.short_description = 'Status'

    def get_created_at(self, obj):
        return obj.created_at
    get_created_at.short_description = 'Created At'

# Registrando as models no admin
admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)