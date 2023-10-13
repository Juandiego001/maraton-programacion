import os
from datetime import datetime

admin = {
    'name': os.getenv('ADMIN_NAME'),
    'username': os.getenv('ADMIN_USERNAME'),
    'password': os.getenv('ADMIN_PASSWORD'),
    'email': os.getenv('ADMIN_EMAIL'),
    'status': os.getenv('ADMIN_STATUS'),
    'created_at': datetime.now(),
    'updated_at': datetime.now(),
    'updated_by': os.getenv('ADMIN_USERNAME')
}