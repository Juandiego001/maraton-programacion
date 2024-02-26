from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId
from app.services import role
from app.services import module


def verify_permission_exists(permissionid: str):
    return mongo.db.permissions.find_one(ObjectId(permissionid))


def create_permission(params: dict):
    if not role.verify_role_exists([{'_id': params['roleid']}]):
        raise HTTPException('El rol no existe')
    
    if not module.verify_module_exists({'_id': params['moduleid']}):
        raise HTTPException('El módulo no existe')
    
    params['updated_at'] = datetime.now()
    params['status'] = True
    created = mongo.db.permissions.insert_one(params)
    if not created:
        raise HTTPException('El módulo no fue creado')
    return created


def update_permission(permissionid: str, params: dict):
    permission = verify_permission_exists(permissionid)
    if not permission:
        raise HTTPException('Permiso no encontrado')
    params['updated_at'] = datetime.now()
    updated = mongo.db.permissions.update_one({'_id': ObjectId(permissionid)},
                                   {'$set': params})
    if not updated:
        raise HTTPException('Permiso no actualizado')
    return updated


def get_permissions_by_role(roleid: str):
    return list(mongo.db.permissions.aggregate([
        {
            '$lookup': {
                'from': 'modules',
                'localField': 'moduleid',
                'foreignField': '_id',
                'as': 'module'
            }
        }, {
            '$unwind': {
                'path': '$module'
            }
        }, {
            '$match': {
                '$expr': {
                    '$eq': [
                        '$roleid', ObjectId(roleid)
                    ]
                }
            }
        },
        {
            '$project': {
                'read': 1,
                'update': 1,
                'create': 1,
                'delete': 1,
                'module': '$module.name'
            }
        }
    ]))


