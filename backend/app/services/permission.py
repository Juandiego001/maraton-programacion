from werkzeug.exceptions import HTTPException
from datetime import datetime
from app import mongo
from bson import ObjectId

def create_permission(params: dict):
    return mongo.db.permissions.insert_one(params)

def update_permission(permissionid: str, params: dict):
    params['updated_at'] = datetime.now()
    updated = mongo.db.permissions.find_one_and_update(
        {'_id': ObjectId(permissionid)}, {'$set': params})
    if not updated:
        raise HTTPException('Permiso no encontrado')
    return updated