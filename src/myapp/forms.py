from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Task

# Formulário de Registro de Usuário
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    

    class Meta:
        model = User
        fields = ['email']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        
        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

# Formulário de Login
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))
    
 

# Formulário de Tarefas
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo', 'descricao', 'stat']  

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.user is None:
            raise forms.ValidationError("Usuário não especificado.")
        return cleaned_data


