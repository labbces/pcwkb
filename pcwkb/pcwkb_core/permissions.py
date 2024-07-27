from rolepermissions.roles import AbstractUserRole

class Revisor(AbstractUserRole):
    available_permissions = {'editar_dados_submetidos': True, 'submeter_dados': True}

class Colaborator(AbstractUserRole):
    available_permissions = {'submeter_dados': True}