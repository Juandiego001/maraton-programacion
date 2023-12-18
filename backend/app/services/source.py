from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId


def create_source(params: dict):
    created = mongo.db.sources.insert_one(params)
    if not created:
        raise Exception('Ocurrió un error al intentar crear el archivo fuente')
    return created


def get_source_by_id(sourceid: str):
    source = mongo.db.sources.find_one(ObjectId(sourceid))
    if not source:
        raise HTTPException('Archivo fuente no encontrado')
    return source


def get_sources():
    return list(mongo.db.sources.find({}))


def get_sources_for_languages(challengeid: str):
    return list(mongo.db.sources.aggregate([
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
                'as': 'challenge'
            }
        }, {
            '$unwind': {
                'path': '$challenge'
            }
        }, {
            '$match': {
                '$expr': {
                    '$eq': [
                        '$challenge._id',
                        ObjectId(challengeid)
                    ]
                }
            }
        }, {
            '$project': {
                '_id': 1,
                'languageid': 1,
                'challengeid': 1,
                'full_source': {
                    '$concat': [
                        '$challenge.name',
                        '$language.extension'
                    ]
                }
            }
        }
    ]))