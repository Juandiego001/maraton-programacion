from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId


def create_difficulty(params: dict):
    difficulty = verify_if_difficulty_exists({'name': params['name']})
    if difficulty:
        raise HTTPException('La dificultad ya existe')
    params['created_at'] = datetime.now()
    params['updated_at'] = datetime.now()

    created = mongo.db.difficulties.insert_one(params)
    if not created:
        raise Exception('Ocurrió un error al intentar crear la dificultad')

    return created


def get_difficulty_by_id(difficultyid: str):
    difficulty = mongo.db.difficulties.find_one(ObjectId(difficultyid))
    if not difficulty:
        raise HTTPException('Dificultad no encontrada')
    return difficulty


def get_difficulties():
    return list(mongo.db.difficulties.find({}))


def verify_if_difficulty_exists(params: dict):
    return mongo.db.difficulties.find_one(params)


def update_difficulty(difficultyid, params):
    difficulty = get_difficulty_by_id(difficultyid)
    if not difficulty:
        raise HTTPException('Dificultad no encontrada')
    if 'name' in params and difficulty['name'] != params['name'] and\
        verify_if_difficulty_exists({'name': params['name']}):
        raise HTTPException('La dificultad ya existe')
    params['updated_at'] = datetime.now()
    updated = mongo.db.difficulties.update_one(
        {'_id': ObjectId(difficultyid)}, {'$set': params})
    if not updated:
        raise HTTPException(
            'Ocurrió un error al intentar actualizar la dificultad')
    return updated

