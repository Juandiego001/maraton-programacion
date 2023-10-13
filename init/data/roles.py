from datetime import datetime
from data.admin import admin

roles = [
    {
        'name': 'Estudiante',
        'status': True,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'updated_by': admin['username']
    },
    {
        'name': 'Administrador',
        'status': True,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'updated_by': admin['username']
    }
]