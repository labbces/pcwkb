# Creating a user using Django shell

Creating a new user:

```python
from pcwkb_core.forms.user_forms import CustomUserCreationForm
```

```python
form_data = {
    'username': 'novousuario',
    'first_name': 'Nome',
    'last_name': 'Sobrenome',
    'email': 'usuario@example.com',
    'password1': 'senha_forte',
    'password2': 'senha_forte'
}

form = CustomUserCreationForm(data=form_data)

if form.is_valid():
    user = form.save()
    print("Usuário criado com sucesso:", user)
else:
    print("Erros ao criar usuário:", form.errors)
```

Giving him reviewer permission:

```python
from rolepermissions.roles import assign_role
from django.contrib.auth import get_user_model

User = get_user_model()

user = User.objects.get(username='<username>')

assign_role(user, 'reviewer')
user.is_staff = True
user.save()
```