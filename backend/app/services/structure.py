from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId

def create_structure(params: dict):
    structure = verify_if_structure_exists(params['title'])
    if structure:
        raise HTTPException('La estructura de datos ya existe')
    params['created_at'] = datetime.now()
    params['updated_at'] = datetime.now()
    created = mongo.db.structures.insert_one(params)
    if not created:
        raise Exception('Ocurrió un error al intentar crear la estructura')
    return created


def get_structure_by_id(structureid: str):
    structure = mongo.db.structures.find_one(ObjectId(structureid))
    if not structure:
        raise HTTPException('Estructura no encontrada')
    return structure


def get_structures():
    return list(mongo.db.structures.find({}))


def verify_if_structure_exists(title: str):
    return mongo.db.structures.find_one({'title': title})


def update_structure(structureid, params):
    structure = get_structure_by_id(structureid)
    if not structure:
        raise HTTPException('Estructura no encontrada')
    
    if 'title' in params and structure['title'] != params['title'] and\
        verify_if_structure_exists(params['title']):
        raise HTTPException('La estructura ya existe')
    
    params['updated_at'] = datetime.now()
    updated = mongo.db.structures.update_one({'_id': ObjectId(structureid)},
                                         {'$set': params})

    if not updated:
        raise HTTPException(
            'Ocurrió un error al intentar actualizar la estructura de datos')
    return updated

