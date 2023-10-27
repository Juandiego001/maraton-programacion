from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId

def create_topics_challenge(params: list):
    return mongo.db.topics_challenge.insert_many(params)

def create_challenge(params: dict):
    challenge = verify_if_challenge_exists(params['title'], params['contestid'])
    if challenge:
        raise HTTPException('La competencia ya existe')
    params['status'] = True
    params['created_at'] = datetime.now()
    params['updated_at'] = datetime.now()

    topicsid = []
    if 'topicsid' in params:
        topicsid = params.pop('topicsid')

    challengeid = mongo.db.challenges.insert_one(params).inserted_id
    if not challengeid:
        raise HTTPException('Ocurrió un error al intentar insertar el reto')
    
    topics_challenge = []
    for topicid in topicsid:
        if not mongo.db.topics.find_one(ObjectId(topicid)):
            raise HTTPException('Hay temáticas asociadas que no existen')
        topics_challenge.append({'challengeid': challengeid,
                                 'topicid': topicid})
    
    if len(topics_challenge):
        create_topics_challenge(topics_challenge)

    return challengeid
    

def get_challenge_by_id(challengeid: str):
    challenge = mongo.db.challenges.aggregate([
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
        }, {
            '$lookup': {
                'from': 'topics_challenge', 
                'localField': '_id', 
                'foreignField': 'challengeid',
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'topics',
                            'localField': 'topicid',
                            'foreignField': '_id',
                            'as': 'topics'
                        }
                    },
                    {
                      '$unwind': {
                        'path': '$topics'
                      }
                    },
                    {
                        '$match': {
                            '$expr': {
                                '$eq': [
                                    '$challengeid', ObjectId(challengeid)
                                ]
                            }
                        }
                    },
                    {
                        '$project': {
                            'topics._id': 1,
                            'topics.title': 1
                        }
                    }
                ],
                'as': 'topics_challenge'
            }
        }, {
            '$match': {
                '$expr': {
                    '$eq': [
                        '$_id', ObjectId(challengeid)
                    ]
                }
            }
        }, {
            '$project': {
                '_id': 1, 
                'title': 1, 
                'source': 1, 
                'created_at': 1,
                'updated_at': 1, 
                'updated_by': 1, 
                'status': 1,
                'contest': {
                    '_id': '$contest._id',
                    'full_contest': {
                        '$concat': [
                            '$contest.platform', ' ', '$contest.made_at']
                    }
                },
                'topics': '$topics_challenge.topics'
            }
        }]).try_next()
    if not challenge:
        raise HTTPException('El reto no fue encontrado')
    return challenge

def get_challenges():
    return list(mongo.db.challenges.aggregate([
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
        }, {
            '$lookup': {
                'from': 'topics_challenge', 
                'localField': '_id', 
                'foreignField': 'challengeid',
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'topics',
                            'localField': 'topicid',
                            'foreignField': '_id',
                            'as': 'topics'
                        }
                    },
                    {
                      '$unwind': {
                        'path': '$topics'
                      }
                    },
                    {
                        '$project': {
                            'topics._id': 1,
                            'topics.title': 1
                        }
                    }
                ],
                'as': 'topics_challenge'
            }
        }, {
            '$project': {
                '_id': 1,
                'title': 1,
                'source': 1,
                'created_at': 1,
                'updated_at': 1, 
                'updated_by': 1, 
                'status': 1,
                'contest': {
                    '_id': '$contest._id',
                    'full_contest': {
                        '$concat': [
                            '$contest.platform', ' ', '$contest.made_at']
                    }
                },
                'topics': '$topics_challenge.topics'
            }
        }]))

def verify_if_challenge_exists(title: str, contestid: ObjectId):
    return mongo.db.challenges.find_one(
        {'$and': [{'title': title}, {'contestid': contestid}]})

def update_challenge(challengeid, params):
    challengeid = ObjectId(challengeid)
    challenge = mongo.db.challenges.find_one({'_id': challengeid})
    if not challenge:
        raise HTTPException('El reto no fue encontrado')
    
    title = ''
    contestid = ''
    if 'title' in params and 'contestid' in params:
        title = params['title']
        contestid = params['contestid']

    if 'title' in params and not 'contestid' in params:
        title = params['title']
        contestid = challenge['contestid']
    
    if 'contestid' in params and not 'title' in params:
        title = challenge['title']
        contestid = params['contestid']

    if title and verify_if_challenge_exists(title, contestid):
        raise HTTPException('El reto ya ha sido registrado')
    
    params['updated_at'] = datetime.now()
    updated = mongo.db.challenges.update_one({'_id': challengeid},
                                             {'$set': params})
    if not updated:
        raise HTTPException('El reto no ha sido actualizado')
    return updated

