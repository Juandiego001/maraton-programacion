from dotenv import load_dotenv
load_dotenv()

import os
from datetime import datetime
from data.admin import admin
from data.roles import roles
from pymongo import MongoClient

mongo: MongoClient = MongoClient(os.getenv('MONGO_URI'))

def delete_data():
    print('Eliminando información...')
    mongo.marathon.users.delete_many({})
    mongo.marathon.user_roles.delete_many({})
    mongo.marathon.roles.delete_many({})
    mongo.marathon.role_permissions.delete_many({})
    mongo.marathon.permissions.delete_many({})

def insert_roles():
    print('Insertando roles...')
    mongo.marathon.roles.insert_many(roles)

def insert_permissions():
    print('Insertando permisos...')
    array_functionalities = ['Roles', 'Estudiantes', 'Estructuras', 'Temáticas',
        'Notificaciones', 'Competencias', 'Retos', 'Soluciones', 'Materiales']
    permissions = []

    for functionality in array_functionalities:
        for action in ['read', 'create', 'update']:
            permissions.append({
                'action': action,
                'functionality': functionality,
                'status': True,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'updated_by': admin['username']
            })
    
    mongo.marathon.permissions.insert_many(permissions)

def insert_role_permissions():
    print('Insertando role_permissions...')
    roles = list(mongo.marathon.roles.find({}, {'_id': 1, 'name': 1}))
    permissions = list(mongo.marathon.permissions.find({}, {'_id': 1,
                                                            'functionality': 1,
                                                            'action': 1}))

    role_permissions = []
    
    for role in roles:
        for permission in permissions:
            if role['name'] == 'Administrador':
                role_permissions.append(
                    {
                        'role_id': role['_id'],
                        'permission_id': permission['_id'],
                        'status': True
                    }
                )
            elif permission['functionality'] in\
                    ['Competencias', 'Retos', 'Soluciones', 'Materiales']:
                role_permissions.append(
                    {
                        'role_id': role['_id'],
                        'permission_id': permission['_id'],
                        'status': True
                    }
                )
    
    mongo.marathon.role_permissions.insert_many(role_permissions)

def insert_admin():
    print('Insertando administrador...')
    adminid = mongo.marathon.users.insert_one(admin).inserted_id
    roleid = mongo.marathon.roles.find_one(
        {'name': 'Administrador'}, {'_id': 1})['_id']
    
    mongo.marathon.user_roles.insert_one({
        'user_id': adminid,
        'role_id': roleid
    })


# Comentar esta opción en caso de no querer eliminar los registros
delete_data()
insert_roles()
insert_permissions()
insert_role_permissions()
insert_admin()
