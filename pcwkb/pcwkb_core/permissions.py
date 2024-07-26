from rolepermissions.roles import AbstractUserRole

class Colaborador(AbstractUserRole):
    available_permissions = {'editar_biomass_gene_assoc': True}
