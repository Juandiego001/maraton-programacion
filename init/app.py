from dotenv import load_dotenv
load_dotenv()

import os
from datetime import datetime
from data.admin import admin
from data.roles import roles
from data.modules import modules
from pymongo import MongoClient


mongo: MongoClient = MongoClient(os.getenv('MONGO_URI'))


def delete_data():
    print('Eliminando información...')
    mongo.marathon.users.delete_many({})
    mongo.marathon.user_roles.delete_many({})
    mongo.marathon.roles.delete_many({})
    mongo.marathon.modules.delete_many({})
    mongo.marathon.permissions.delete_many({})


def insert_roles():
    print('Insertando roles...')
    mongo.marathon.roles.insert_many(roles)


def insert_modules():
    print('Insertando modulos...')
    mongo.marathon.modules.insert_many(modules)


def insert_permissions():
    print('Insertando permisos...')
    roles = list(mongo.marathon.roles.find({}, {'_id': 1, 'name': 1}))
    modules = list(mongo.marathon.modules.find({}, {'_id': 1, 'name': 1} ))
    permissions = []

    for role in roles:
        for module in modules:
            if role['name'] == 'Administrador':
                permissions.append({
                    'roleid': role['_id'],
                    'moduleid': module['_id'],
                    'read': True,
                    'create': True,
                    'update': True,
                    'delete': True,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now(),
                    'updated_by': admin['username']
                })
            elif role['name'] == 'Estudiante':
                if module['name'] in ['Competencias', 'Retos', 'Soluciones', 
                                      'Materiales']:
                    permissions.append({
                        'roleid': role['_id'],
                        'moduleid': module['_id'],
                        'read': True,
                        'create': True,
                        'update': True,
                        'delete': False,
                        'created_at': datetime.now(),
                        'updated_at': datetime.now(),
                        'updated_by': admin['username']
                    })
                else:
                    permissions.append({
                        'roleid': role['_id'],
                        'moduleid': module['_id'],
                        'read': False,
                        'create': False,
                        'update': False,
                        'delete': False,
                        'created_at': datetime.now(),
                        'updated_at': datetime.now(),
                        'updated_by': admin['username']
                    })
    
    mongo.marathon.permissions.insert_many(permissions)


def insert_admin():
    print('Insertando administrador...')
    adminid = mongo.marathon.users.insert_one(admin).inserted_id
    roleid = mongo.marathon.roles.find_one(
        {'name': 'Administrador'}, {'_id': 1})['_id']
    
    mongo.marathon.user_roles.insert_one({
        'userid': adminid,
        'roleid': roleid
    })


# Comentar esta opción en caso de no querer eliminar los registros
delete_data()
insert_roles()
insert_modules()
insert_permissions()
insert_admin()
