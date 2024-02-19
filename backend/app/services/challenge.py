from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId

def create_topics_challenge(params: list):
    return mongo.db.topics_challenge.insert_many(params)

def create_languages_challenge(params: list):
    return mongo.db.sources.insert_many(params)

def create_challenge(params: dict):
    challenge = verify_if_challenge_exists(params['title'], params['contestid'])
    if challenge:
        raise HTTPException('La competencia ya existe')
    params['status'] = True
    params['created_at'] = datetime.now()
    params['updated_at'] = datetime.now()

    languagesid = []
    if 'languagesid' in params:
        languagesid = params.pop('languagesid')

    topicsid = []
    if 'topicsid' in params:
        topicsid = params.pop('topicsid')

    challengeid = mongo.db.challenges.insert_one(params).inserted_id
    if not challengeid:
        raise HTTPException('Ocurrió un error al intentar insertar el reto')
    
    languages_challenge = []
    for languageid in languagesid:
        if not mongo.db.languages.find_one(ObjectId(languageid)):
            raise HTTPException('Hay lenguajes asociados que no existen')
        languages_challenge.append({'challengeid': challengeid,
                                 'languageid': languageid})
    
    if len(languages_challenge):
        create_languages_challenge(languages_challenge)

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
            '$lookup': {
                'from': 'sources',
                'localField': '_id',
                'foreignField': 'challengeid',
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'languages',
                            'localField': 'languageid',
                            'foreignField': '_id',
                            'as': 'languages'
                        }
                    }, {
                        '$unwind': {
                            'path': '$languages'
                        }
                    }
                ],
                'as': 'sources'
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
                'name': 1, 
                'created_at': 1,
                'updated_at': 1, 
                'updated_by': 1, 
                'status': 1,
                'languagesid': '$sources.languages._id',
                'difficultyid': 1,
                'contestid': '$contest._id',
                'topicsid': '$topics_challenge.topics._id',
                'contest': {
                    '_id': '$contest._id',
                    'full_contest': {
                        '$concat': [
                            '$contest.platform', ' ', {
                                '$dateToString': {
                                    'date': '$contest.made_at',
                                    'format': '%Y-%m-%d'
                                    }
                                }]
                    }
                },
                'topics': '$topics_challenge.topics'
            }
        }, {
            '$sort': {
                'contest.made_at': -1
            }
        }]).try_next()
    if not challenge:
        raise HTTPException('El reto no fue encontrado')
    return challenge

def get_challenges(query: dict):
    filter = {}
    if 'title' in query:
        filter['title'] = {
            '$regex':  f'{query["title"]}',
            '$options': 'i'
        }
    if 'contestid' in query:
        filter['contest._id'] = query['contestid']
    if 'difficultyid' in query:
        filter['difficulty._id'] = query['difficultyid']
    if 'topicsid' in query:
        filter['topics_challenge.topics._id'] = {
            '$in': [ObjectId(id) for id in query['topicsid'].split(',')]
        }

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
            '$lookup': {
                'from': 'difficulties',
                'localField': 'difficultyid',
                'foreignField': '_id',
                'as': 'difficulty'
            }
        }, {
            '$match': filter
        }, {
            '$project': {
                '_id': 1,
                'title': 1,
                'source': 1,
                'created_at': 1,
                'updated_at': 1, 
                'updated_by': 1, 
                'status': 1,
                'difficulty': 1,
                'contestid': '$contest._id',
                'topicsid': '$topics_challenge.topics._id',
                'full_contest': {
                    '$concat': [ '$contest.platform', ' ', {
                        '$dateToString': {
                            'date': '$contest.made_at',
                            'format': '%Y-%m-%d'
                            }
                        }]
                },
                'contest_url': '$contest.file_url',
                'contest_link': '$contest.link',
                'topics': '$topics_challenge.topics'
            }
        }]))

def verify_if_challenge_exists(title: str, contestid: ObjectId):
    return mongo.db.challenges.find_one(
        {'$and': [{'title': title}, {'contestid': contestid}]})

def validate_changing_title_contest(params, challenge):
    title = ''
    contestid = ''
    if 'title' in params and params['title'] != challenge['title']:
        title = params['title']
        if 'contestid' in params and\
            params['contestid'] != challenge['contestid']:
            contestid = params['contestid']
        else:
            contestid = challenge['contestid']
    elif not 'title' in params:
        if 'contestid' in params and\
            params['contestid'] != challenge['contestid']:
            title = challenge['title']
            contestid = params['contestid']
    
    return title, contestid

def update_challenge(challengeid, params):
    challengeid = ObjectId(challengeid)
    challenge = mongo.db.challenges.find_one({'_id': challengeid})
    if not challenge:
        raise HTTPException('El reto no fue encontrado')
    
    title, contestid = validate_changing_title_contest(params, challenge)
    if title and verify_if_challenge_exists(title, contestid):
        raise HTTPException('El reto ya ha sido registrado')
    
    if 'languagesid' in params:
        mongo.db.sources.delete_many({'challengeid': challengeid})
        mongo.db.sources.insert_many([
            {'challengeid': challengeid,
                'languageid': languageid}
        for languageid in params['languagesid']])

    if 'topicsid' in params:
        mongo.db.topics_challenge.delete_many({'challengeid': challengeid})
        mongo.db.topics_challenge.insert_many([
            {'challengeid': challengeid,
                'topicid': topicid}
        for topicid in params['topicsid']])
    
    params['updated_at'] = datetime.now()
    updated = mongo.db.challenges.update_one({'_id': challengeid},
                                             {'$set': params})
    if not updated:
        raise HTTPException('El reto no ha sido actualizado')
    return updated


def get_challenges_by_contest(contestid: str):
    return list(mongo.db.challenges.find({'contestid': ObjectId(contestid)}))
