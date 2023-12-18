from datetime import datetime, date
import io
from werkzeug.exceptions import HTTPException
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from app import mongo, dbx
from bson import ObjectId
from app.utils import generate_id
import dropbox


def put_file(file: FileStorage, materialid: str):
    real_name = secure_filename(file.filename)
    format = real_name.split('.')[-1]
    dbx.files_upload(file.read(),
                     f'/contests/{materialid}.{format}',
                     mode=dropbox.files.WriteMode.overwrite)
    return real_name


def create_contest(params: dict):
    contestid = ObjectId()
    params['_id'] = contestid
    params['real_name'] = put_file(params.pop('file'), contestid)\
      if 'file' in params else None
    params['file_url'] = f'{contestid}?v={generate_id()}'
    params['created_at'] = params['updated_at'] = datetime.now()
    params['status'] = True
    created = mongo.db.contests.insert_one(params)
    if not created:
        raise HTTPException('La competencia no fue creada')
    return created


def verify_exists(contestid: str):
    return mongo.db.contests.find_one({'_id': ObjectId(contestid)})


def get_contest_by_id(contestid: str):
    return mongo.db.contests.find_one(ObjectId(contestid))


def get_contests(query: dict):
    full_query = {}
    if 'initial_date' in query and 'end_date' in query:
        full_query['made_at'] = {
            '$gt': query['initial_date'],
            '$lt': query['end_date']
        }
    return list(mongo.db.contests.find(full_query))


def update_contest(contestid, params):
    contest = verify_exists(contestid)
    if not contest:
        raise HTTPException('La competencia no ha sido encontrada')
    if 'file' in params:
        params['real_name'] = put_file(params.pop('file'), contestid)
        params['file_url'] = f'{contestid}?v={generate_id()}'
    params['updated_at'] = datetime.now()
    updated = mongo.db.contests.find_one_and_update(
        {'_id': ObjectId(contestid)}, {'$set': params})
    if not updated:
        raise HTTPException('Competencia no actualizada')
    return updated


def download_contest(contestid: str):
    contest = verify_exists(contestid)
    if not contest:
        raise HTTPException('Material no encontrado')
    format = contest['real_name'].split('.')[-1]
    md, file = dbx.files_download(
        f'/contests/{contestid}.{format}')
    return io.BytesIO(file.content), contest['real_name']
