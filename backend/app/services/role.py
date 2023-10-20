from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId

def create_rol(params: dict):
    if verify_exists([{'name': params['name']}]):
        raise HTTPException('El rol ya ha sido creado')
    params['created_at'] = params['updated_at'] = datetime.now()
    params['status'] = True
    return mongo.db.roles.insert_one(params)

def verify_exists(params: list):
    return mongo.db.roles.find_one({'$or': params})

def get_roles():
    return mongo.db.roles.find({})

def get_role_by_id(roleid: str):
    role = verify_exists([{'_id': ObjectId(roleid)}])
    if not role:
        raise HTTPException('Rol no encontrado')
    return role

def update_role(roleid:str, params: dict):
    params['updated_at'] = datetime.now()
    updated = mongo.db.roles.find_one_and_update({'_id': ObjectId(roleid)},
                                                 {'$set': params})
    if not updated:
        raise HTTPException('Rol no encontrado')
    return updated

