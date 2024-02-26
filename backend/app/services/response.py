from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId

def create_response(params: dict):
    response = verify_if_response_exists(params['code'])
    if response:
        raise HTTPException('La respuesta del juez ya existe')
    params['created_at'] = datetime.now()
    params['updated_at'] = datetime.now()
    created = mongo.db.responses.insert_one(params)
    if not created:
        raise Exception(
            'Ocurrió un error al intentar crear la respuesta del juez')
    return created


def get_response_by_id(responseid: str):
    response = mongo.db.responses.find_one(ObjectId(responseid))
    if not response:
        raise HTTPException('Respuesta del juez no encontrado')
    return response


def get_responses():
    return list(mongo.db.responses.find({}))


def verify_if_response_exists(code: str):
    return mongo.db.responses.find_one({'code': code})


def update_response(responseid, params):
    response = get_response_by_id(responseid)
    if not response:
        raise HTTPException('Respuesta del juez no encontrada')
    
    if 'code' in params and response['code'] != params['code'] and\
        verify_if_response_exists(params['code']):
        raise HTTPException('La respuesta del juez ya existe')
    
    params['updated_at'] = datetime.now()
    updated = mongo.db.responses.update_one({'_id': ObjectId(responseid)},
                                         {'$set': params})

    if not updated:
        raise HTTPException(
            'Ocurrió un error al intentar actualizar la respuesta del juez')
    return updated

