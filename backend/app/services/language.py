from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId


def create_language(params: dict):
    language = verify_if_language_exists({'name': params['name']})
    if language:
        raise HTTPException('El lenguaje ya existe')
    params['created_at'] = datetime.now()
    params['updated_at'] = datetime.now()

    created = mongo.db.languages.insert_one(params)
    if not created:
        raise Exception('Ocurrió un error al intentar crear el lenguaje')

    return created


def get_language_by_id(languageid: str):
    language = mongo.db.languages.find_one(ObjectId(languageid))
    if not language:
        raise HTTPException('Lenguaje no encontrado')
    return language


def get_languages():
    return list(mongo.db.languages.find({}))


def verify_if_language_exists(params: dict):
    return mongo.db.languages.find_one(params)


def update_language(languageid, params):
    language = get_language_by_id(languageid)
    if not language:
        raise HTTPException('Lenguaje no encontrado')
    if 'name' in params and language['name'] != params['name'] and\
        verify_if_language_exists({'name': params['name']}):
        raise HTTPException('El lenguaje ya existe')
    params['updated_at'] = datetime.now()
    updated = mongo.db.languages.update_one(
        {'_id': ObjectId(languageid)}, {'$set': params})
    if not updated:
        raise HTTPException(
            'Ocurrió un error al intentar actualizar el lenguaje')
    return updated

