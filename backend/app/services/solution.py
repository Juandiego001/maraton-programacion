from datetime import datetime
import hashlib
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException
from app import mongo, dbx
from bson import ObjectId
from app.services.language import verify_if_language_exists
from werkzeug.utils import secure_filename
from app.utils import generate_id


def put_file(file: FileStorage, solutionid: str):
    real_name = secure_filename(file.filename)
    format = real_name.split('.')[-1]
    dbx.files_upload(file.read(),
                     f'/solutions/{solutionid}.{format}')
    return real_name


def create_solution(params: dict):
    if not verify_if_language_exists({'_id': ObjectId(params['languageid'])}):
        raise HTTPException('El lenguaje asociado a la solución no existe')
    solutionid = ObjectId()
    params['_id'] = solutionid
    params['real_name'] = put_file(params.pop('file'), solutionid)\
      if 'file' in params else None
    params['file_url'] = f'{solutionid}?v={generate_id()}'
    params['created_at'] = params['updated_at'] = datetime.now()
    params['status'] = True
    created = mongo.db.solutions.insert_one(params)
    if not created:
        raise HTTPException('La solución no fue creada')
    return created


def verify_exists(params: list):
    return mongo.db.solutions.find_one({'$or': params})


def get_solutions():
    return mongo.db.solutions.find({})


def get_solution_by_id(solutionid: str):
    solution = verify_exists([{'_id': ObjectId(solutionid)}])
    if not solution:
        raise HTTPException('Solución no encontrada')
    return solution


def update_solution(solutionid: str, params: dict):
    solution = verify_exists([{'_id': ObjectId(solutionid)}])
    if not solution:
        raise HTTPException('Solución no encontrada')
    params['real_name'] = put_file(params.pop('file'), solutionid)\
      if 'file' in params else None
    params['file_url'] = f'{solutionid}?v={generate_id()}'    
    params['updated_at'] = datetime.now()
    updated = mongo.db.solutions.find_one_and_update(
        {'_id': ObjectId(solutionid)}, {'$set': params})
    if not updated:
        raise HTTPException('Solución no encontrada')
    return updated

