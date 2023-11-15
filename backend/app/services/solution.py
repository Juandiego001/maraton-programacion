from datetime import datetime
import io
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException
from app import mongo, dbx
from bson import ObjectId
from app.services.language import verify_if_language_exists
from werkzeug.utils import secure_filename
from app.utils import generate_id
import dropbox


def put_file(file: FileStorage, solutionid: str):
    real_name = secure_filename(file.filename)
    format = real_name.split('.')[-1]
    dbx.files_upload(file.read(),
                     f'/solutions/{solutionid}.{format}',
                     mode=dropbox.files.WriteMode.overwrite)
    return real_name


def create_solution(params: dict):
    print('params********', params)
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
    return list(mongo.db.solutions.aggregate([
        {
            '$lookup': {
                'from': 'languages',
                'localField': 'languageid',
                'foreignField': '_id',
                'as': 'language'
            }
        }, {
            '$unwind': {
                'path': '$language'
            }
        }, {
            '$lookup': {
                'from': 'challenges',
                'localField': 'challengeid',
                'foreignField': '_id',
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'contests',
                            'localField': 'contestid',
                            'foreignField': '_id',
                            'as': 'contest'
                        }
                    }, {
                        '$unwind': {
                            'path': '$contest'
                        }
                    }
                ],
                'as': 'challenge'
            }
        }, {
            '$unwind': {
                'path': '$challenge'
            }
        }, {
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
                'real_name': 1,
                'language': '$language.name',
                'full_challenge': {
                    '$concat': [
                        '$challenge.title',
                        ' - ',
                        '$challenge.contest.platform',
                        ' ',
                        '$challenge.contest.made_at'
                    ]
                },
                'username': '$user.username'
            }
        }
    ]))


def get_solution_by_id(solutionid: str):
    solution = verify_exists([{'_id': ObjectId(solutionid)}])
    if not solution:
        raise HTTPException('Solución no encontrada')
    return solution


def update_solution(solutionid: str, params: dict):
    solution = verify_exists([{'_id': ObjectId(solutionid)}])
    if not solution:
        raise HTTPException('Solución no encontrada')
    if 'file' in params:
        params['real_name'] = put_file(params.pop('file'), solutionid)
        params['file_url'] = f'{solutionid}?v={generate_id()}'

    params['updated_at'] = datetime.now()
    updated = mongo.db.solutions.find_one_and_update(
        {'_id': ObjectId(solutionid)}, {'$set': params})
    if not updated:
        raise HTTPException('Solución no encontrada')
    return updated


def download_solution(solutionid: str):
    solution = verify_exists([{'_id': ObjectId(solutionid)}])
    if not solution:
        raise HTTPException('Solución no encontrada')
    format = solution['real_name'].split('.')[-1]
    md, file = dbx.files_download(
        f'/solutions/{solutionid}.{format}')
    return io.BytesIO(file.content), solution['real_name']