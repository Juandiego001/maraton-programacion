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


# Valida que la competencia no esté registrada
def validate_exists(platform: str, name: str, made_at: datetime.date):
    return mongo.db.contests.find_one({'platform': platform, 
                                       'name': name,
                                       'made_at': made_at})


def create_contest(params: dict):
    contestid = ObjectId()
    params['_id'] = contestid
    params['real_name'] = put_file(params.pop('file'), contestid)\
      if 'file' in params else None
    params['file_url'] = f'{contestid}?v={generate_id()}'\
        if 'file' in params else None
    params['created_at'] = params['updated_at'] = datetime.now()
    params['status'] = True

    if validate_exists(params['platform'], params['name'], params['made_at']):
        raise HTTPException('La competencia ya ha sido registrada')
    created = mongo.db.contests.insert_one(params)
    if not created:
        raise HTTPException('La competencia no fue creada')
    return created


def verify_exists(contestid: str):
    return mongo.db.contests.find_one({'_id': ObjectId(contestid)})


def get_contest_by_id(contestid: str):
    return mongo.db.contests.find_one(ObjectId(contestid))


def get_contests(query: dict):
    filter = {}
    if 'platform' in query:
        filter['platform'] = {
            '$regex':  f'{query["platform"]}',
            '$options': 'i'
        }
    if 'name' in query:
        filter['name'] = {
            '$regex': f'{query["name"]}',
            '$options': 'i'
        }
    if 'initial_date' in query or 'end_date' in query:
        filter['made_at'] = {}
    if 'initial_date' in query:
        filter['made_at']['$gte'] = query['initial_date']
    if 'end_date' in query:
        filter['made_at']['$lte'] = query['end_date']
    if 'isTraining' in query:
        filter['isTraining'] = query['isTraining']

    return list(mongo.db.contests.find(filter).sort('made_at', -1))


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
