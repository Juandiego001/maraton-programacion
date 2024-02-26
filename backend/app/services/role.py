from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId
from app.services.module import get_modules


def create_default_permissions(roleid: str, updated_by: str):
    modules = get_modules()
    permissions = []
    for module in modules:
        permissions.append({
            'roleid': ObjectId(roleid),
            'moduleid': ObjectId(module['_id']),
            'read': False,
            'create': False,
            'update': False,
            'delete': False,
            'updated_at': datetime.now(),
            'updated_by': updated_by
        })
    
    return mongo.db.permissions.insert_many(permissions)


def create_rol(params: dict):
    if verify_role_exists([{'name': params['name']}]):
        raise HTTPException('El rol ya ha sido creado')
    params['created_at'] = params['updated_at'] = datetime.now()
    params['status'] = True
    roleid = mongo.db.roles.insert_one(params).inserted_id
    if not roleid:
        raise HTTPException('El rol no fue creado')
    permissions_created = create_default_permissions(roleid,
                                                     params['updated_by'])
    if not permissions_created:
        raise HTTPException('No se crearon los permisos por defecto del rol')
    return permissions_created


def verify_role_exists(params: list):
    return mongo.db.roles.find_one({'$or': params})


def get_roles():
    return mongo.db.roles.find({})


def get_role_by_id(roleid: str):
    role = verify_role_exists([{'_id': ObjectId(roleid)}])
    if not role:
        raise HTTPException('Rol no encontrado')
    return role


def update_role(roleid:str, params: dict):
    role = verify_role_exists([{'_id': ObjectId(roleid)}])
    if not role:
        raise HTTPException('Rol no encontrado')
    
    if 'name' in params and role['name'] != params['name'] and\
        verify_role_exists([{'name': params['name']}]):
        raise HTTPException('El rol ya existe')

    params['updated_at'] = datetime.now()
    updated = mongo.db.roles.find_one_and_update({'_id': ObjectId(roleid)},
                                                 {'$set': params})
    if not updated:
        raise HTTPException('Rol no encontrado')
    return updated

