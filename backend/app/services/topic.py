from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId

def create_topic(params: dict):
    topic = verify_if_topic_exists(params['title'])
    if topic:
        raise HTTPException('La temática ya existe')
    params['created_at'] = datetime.now()
    params['updated_at'] = datetime.now()

    created = mongo.db.topics.insert_one(params)
    if not created:
        raise Exception('Ocurrió un error al intentar crear la temática')

    return created


def get_topic_by_id(topicid: str):
    topic = mongo.db.topics.find_one(ObjectId(topicid))
    if not topic:
        raise HTTPException('Temática no encontrada')
    return topic


def get_topics():
    return list(mongo.db.topics.find({}))


def verify_if_topic_exists(title: str):
    return mongo.db.topics.find_one({'title': title})


def update_topic(topicid, params):
    topic = get_topic_by_id(topicid)
    if not topic:
        raise HTTPException('Temática no encontrada')
    
    if 'title' in params and topic['title'] != params['title'] and\
        verify_if_topic_exists(params['title']):
        raise HTTPException('La temática ya existe')
    
    params['updated_at'] = datetime.now()
    updated = mongo.db.topics.update_one({'_id': ObjectId(topicid)},
                                         {'$set': params})

    if not updated:
        raise HTTPException(
            'Ocurrió un error al intentar actualizar la temática')
    return updated

