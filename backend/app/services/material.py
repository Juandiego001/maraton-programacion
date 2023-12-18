from datetime import datetime
import io
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException
from app import mongo, dbx
from bson import ObjectId
from app.services.user import verify_if_user_exists
from werkzeug.utils import secure_filename
from app.utils import generate_id
import dropbox


def put_file(file: FileStorage, materialid: str):
    real_name = secure_filename(file.filename)
    format = real_name.split('.')[-1]
    dbx.files_upload(file.read(),
                     f'/materials/{materialid}.{format}',
                     mode=dropbox.files.WriteMode.overwrite)
    return real_name


def create_material(params: dict):
    if not verify_if_user_exists([{'_id': ObjectId(params['userid'])}]):
        raise HTTPException('Usuario asociado al material no encontrado')
    materialid = ObjectId()
    params['_id'] = materialid
    params['real_name'] = put_file(params.pop('file'), materialid)\
      if 'file' in params else None
    params['file_url'] = f'{materialid}?v={generate_id()}'
    params['created_at'] = params['updated_at'] = datetime.now()
    params['status'] = True
    created = mongo.db.materials.insert_one(params)
    if not created:
        raise HTTPException('El material no fue creado')
    return created


def verify_exists(materialid: str):
    return mongo.db.materials.find_one({'_id': ObjectId(materialid)})


def get_materials():
    return list(mongo.db.materials.aggregate([
        {
            '$lookup': {
                'from': 'users',
                'localField': 'userid',
                'foreignField': '_id',
                'as': 'user'
            }
        }, {
            '$unwind': {
                'path': '$user'
            }
        }, {
            '$project': {
                'username': '$user.username',
                'real_name': 1,
                'file_url': 1,
                'link': 1,
                'description': 1,
                'status': 1
            }
        }
    ]))


def get_material(materialid: str):
    return mongo.db.materials.aggregate([
        {
            '$lookup': {
                'from': 'users',
                'localField': 'userid',
                'foreignField': '_id',
                'as': 'user'
            }
        }, {
            '$unwind': {
                'path': '$user'
            }
        }, {
            '$match': {
                '$expr': {
                    '$eq': [
                        '$_id', ObjectId(materialid)
                    ]
                }
            }
        }, {
            '$project': {
                'username': '$user.username',
                'real_name': 1,
                'file_url': 1,
                'link': 1,
                'description': 1,
                'status': 1
            }
        }
    ]).try_next()


def get_material_by_id(materialid: str):
    material = verify_exists(materialid)
    if not material:
        raise HTTPException('Material no encontrado')
    return get_material(materialid)


def update_material(materialid: str, params: dict):
    material = verify_exists(materialid)
    if not material:
        raise HTTPException('Material no encontrado')
    if 'file' in params:
        params['real_name'] = put_file(params.pop('file'), materialid)
        params['file_url'] = f'{materialid}?v={generate_id()}'
    params['updated_at'] = datetime.now()
    updated = mongo.db.materials.find_one_and_update(
        {'_id': ObjectId(materialid)}, {'$set': params})
    if not updated:
        raise HTTPException('Material no actualizado')
    return updated


def download_material(materialid: str):
    material = verify_exists(materialid)
    if not material:
        raise HTTPException('Material no encontrado')
    format = material['real_name'].split('.')[-1]
    md, file = dbx.files_download(
        f'/materials/{materialid}.{format}')
    return io.BytesIO(file.content), material['real_name']


def delete_file(materialid: str):
    material = verify_exists(materialid)
    if not material:
        raise HTTPException('Material no encontrado')
    format = material['real_name'].split('.')[-1]
    was_deleted = dbx.files_delete(
        f'/materials/{materialid}.{format}')
    if not was_deleted:
        raise HTTPException('Material no eliminado')
    was_deleted = mongo.db.materials.delete_one(
        {'_id': ObjectId(materialid)})
    if not was_deleted:
        raise HTTPException('El material no fue eliminado de la base de datos')
    return was_deleted
    
