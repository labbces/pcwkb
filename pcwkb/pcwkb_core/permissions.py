from rolepermissions.roles import AbstractUserRole

class Reviewer(AbstractUserRole):
    available_permissions = {'edit_submitted_data': True, 'submit_data': True}

class Researcher(AbstractUserRole):
    available_permissions = {'submit_data': True}