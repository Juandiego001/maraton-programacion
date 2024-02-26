from datetime import datetime
import io
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException
from app import mongo, dbx
from bson import ObjectId
from app.services.language import verify_if_language_exists
from werkzeug.utils import secure_filename
from app.utils import generate_id
import dropbox


def create_topics_solution(params: list):
    return mongo.db.topics_solution.insert_many(params)


def create_structures_solution(params: list):
    return mongo.db.structures_solution.insert_many(params)


def put_file(file: FileStorage, solutionid: str):
    real_name = secure_filename(file.filename)
    format = real_name.split('.')[-1]
    dbx.files_upload(file.read(),
                     f'/solutions/{solutionid}.{format}',
                     mode=dropbox.files.WriteMode.overwrite)
    return real_name


def create_solution(params: dict):
    solutionid = ObjectId()
    params['_id'] = solutionid
    params['real_name'] = put_file(params.pop('file'), solutionid)\
      if 'file' in params else None
    params['file_url'] = f'{solutionid}?v={generate_id()}'\
      if 'file' in params else None
    params['created_at'] = params['updated_at'] = datetime.now()
    params['status'] = True

    structuresid = []
    if 'structuresid' in params:
        structuresid = params.pop('structuresid')

    topicsid = []
    if 'topicsid' in params:
        topicsid = params.pop('topicsid')

    solutionid = mongo.db.solutions.insert_one(params).inserted_id
    if not solutionid:
        raise HTTPException('La solución no fue creada')

    structures_solution = []
    for structureid in structuresid:
        if not mongo.db.structures.find_one(ObjectId(structureid)):
            raise HTTPException('Hay estructuras asociadas que no existen')
        structures_solution.append({'solutionid': solutionid,
                                 'structureid': structureid})

    if len(structures_solution):
        create_structures_solution(structures_solution)

    topics_solution = []
    for topicid in topicsid:
        if not mongo.db.topics.find_one(ObjectId(topicid)):
            raise HTTPException('Hay temáticas asociadas que no existen')
        topics_solution.append({'solutionid': solutionid,
                                 'topicid': topicid})

    if len(topics_solution):
        create_topics_solution(topics_solution)

    return solutionid


def verify_exists(params: list):
    return mongo.db.solutions.find_one({'$or': params})


def get_solution(solutionid: str):
    return mongo.db.solutions.aggregate([
        {
            '$lookup': {
                'from': 'users',
                'localField': 'userid',
                'foreignField': '_id',
                'as': 'user'
            }
        }, {
            '$unwind': {
                'path': '$user'
            }
        }, {
            '$lookup': {
                'from': 'sources',
                'localField': 'sourceid',
                'foreignField': '_id',
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'challenges',
                            'localField': 'challengeid',
                            'foreignField': '_id',
                            'pipeline': [
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
                                }
                            ],
                            'as': 'challenge'
                        }
                    }, {
                        '$unwind': {
                            'path': '$challenge'
                        }
                    }, {
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
                    }
                ],
                'as': 'source'
            }
        }, {
            '$unwind': {
                'path': '$source'
            }
        }, {
            '$lookup': {
                'from': 'topics_solution', 
                'localField': '_id', 
                'foreignField': 'solutionid',
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
                                    '$solutionid', ObjectId(solutionid)
                                ]
                            }
                        }
                    },
                    {
                        '$project': {
                            'topics._id': 1
                        }
                    }
                ],
                'as': 'topics_solution'
            }
        }, {
            '$lookup': {
                'from': 'structures_solution', 
                'localField': '_id', 
                'foreignField': 'solutionid',
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'structures',
                            'localField': 'structureid',
                            'foreignField': '_id',
                            'as': 'structures'
                        }
                    },
                    {
                      '$unwind': {
                        'path': '$structures'
                      }
                    },
                    {
                        '$match': {
                            '$expr': {
                                '$eq': [
                                    '$solutionid', ObjectId(solutionid)
                                ]
                            }
                        }
                    },
                    {
                        '$project': {
                            'structures._id': 1,
                        }
                    }
                ],
                'as': 'structures_solution'
            }
        }, {
            '$lookup': {
                'from': 'responses',
                'localField': 'responseid',
                'foreignField': '_id',
                'as': 'response'
            }
        }, {
            '$unwind': {
                'preserveNullAndEmptyArrays': True,
                'path': '$response'
            }
        }, {
            '$match': {
                '$expr': {
                    '$eq': [
                        '$_id',
                        ObjectId(solutionid)
                    ]
                }
            }
        }, {
            '$project': {
                'real_name': 1,
                'link': 1,
                'sourceid': 1,
                'full_source': {
                    '$concat': [
                        '$source.challenge.name',
                        '$source.language.extension'
                    ]
                },
                'contestid': '$source.challenge.contest._id',
                'full_contest': {
                    '$concat': [
                        '$source.challenge.contest.platform',
                        ' - ',
                        {
                            '$dateToString': {
                                'date': '$source.challenge.contest.made_at',
                                'format': '%Y-%m-%d'
                            }
                        }
                    ]
                },
                'challengeid': '$source.challenge._id',
                'full_challenge': '$source.challenge.name',
                'username': '$user.username',
                'topicsid': '$topics_solution.topics._id',
                'structuresid': '$structures_solution.structures._id',
                'responseid': 1,
                'description': 1,
                'status': 1,
                'updated_at': 1, 
                'updated_by': 1
            }
        }
    ]).try_next()


def get_solutions(query: dict):
    filter = {}
    if 'contestid' in query:
        filter['source.challenge.contest._id'] = ObjectId(query['contestid'])
    if 'challengeid' in query:
        filter['source.challenge._id'] = ObjectId(query['challengeid'])
    if 'languageid' in query:
        filter['source.language._id'] = ObjectId(query['languageid'])
    return list(mongo.db.solutions.aggregate([
        {
            '$lookup': {
                'from': 'users',
                'localField': 'userid',
                'foreignField': '_id',
                'as': 'user'
            }
        }, {
            '$unwind': {
                'path': '$user'
            }
        }, {
            '$lookup': {
                'from': 'sources',
                'localField': 'sourceid',
                'foreignField': '_id',
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'challenges',
                            'localField': 'challengeid',
                            'foreignField': '_id',
                            'pipeline': [
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
                                }
                            ],
                            'as': 'challenge'
                        }
                    }, {
                        '$unwind': {
                            'path': '$challenge'
                        }
                    }, {
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
                    }
                ],
                'as': 'source'
            }
        }, {
            '$unwind': {
                'path': '$source'
            }
        }, {
            '$lookup': {
                'from': 'topics_solution', 
                'localField': '_id', 
                'foreignField': 'solutionid',
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
                'as': 'topics_solution'
            }
        }, {
            '$lookup': {
                'from': 'structures_solution', 
                'localField': '_id', 
                'foreignField': 'solutionid',
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'structures',
                            'localField': 'structureid',
                            'foreignField': '_id',
                            'as': 'structures'
                        }
                    },
                    {
                      '$unwind': {
                        'path': '$structures'
                      }
                    },
                    {
                        '$project': {
                            'structures._id': 1,
                            'structures.title': 1
                        }
                    }
                ],
                'as': 'structures_solution'
            }
        }, {
            '$lookup': {
                'from': 'responses',
                'localField': 'responseid',
                'foreignField': '_id',
                'as': 'response'
            }
        }, {
            '$unwind': {
                'preserveNullAndEmptyArrays': True,
                'path': '$response'
            }
        }, {
            '$match': filter
        }, {
            '$project': {
                'file_url': 1,
                'real_name': 1,
                'link': 1,
                'full_response': '$response.code',
                'full_source': {
                    '$concat': [
                        '$source.challenge.name',
                        '$source.language.extension'
                    ]
                },
                'full_contest': {
                    '$concat': [
                        '$source.challenge.contest.platform',
                        ' - ',
                        {
                            '$dateToString': {
                                'date': '$source.challenge.contest.made_at',
                                'format': '%Y-%m-%d'
                                }
                            }
                    ]
                },
                'full_challenge': '$source.challenge.name',
                'topicsid': '$topics_solution.topics._id',
                'username': '$user.username'
            }
        }
    ]))


def get_solution_by_id(solutionid: str):
    solution = verify_exists([{'_id': ObjectId(solutionid)}])
    if not solution:
        raise HTTPException('Solución no encontrada')
    return get_solution(solutionid)


def update_solution(solutionid: str, params: dict):
    solutionid = ObjectId(solutionid)
    solution = verify_exists([{'_id': solutionid}])
    if not solution:
        raise HTTPException('Solución no encontrada')
    if 'file' in params:
        params['real_name'] = put_file(params.pop('file'), solutionid)
        params['file_url'] = f'{solutionid}?v={generate_id()}'

    if 'structuresid' in params:
        mongo.db.structures_solution.delete_many(
            {'solutionid': solutionid})
        mongo.db.structures_solution.insert_many([
            {'solutionid': solutionid,
                'structureid': structureid}
        for structureid in params['structuresid']])

    if 'topicsid' in params:
        mongo.db.topics_solution.delete_many(
            {'solutionid': solutionid})
        mongo.db.topics_solution.insert_many([
            {'solutionid': solutionid,
                'topicid': topicid}
        for topicid in params['topicsid']])

    params['updated_at'] = datetime.now()
    updated = mongo.db.solutions.find_one_and_update(
        {'_id': solutionid}, {'$set': params})
    
    if not updated:
        raise HTTPException('La solución no ha sido actualizada')
    return updated


def download_solution(solutionid: str):
    solution = verify_exists([{'_id': ObjectId(solutionid)}])
    if not solution:
        raise HTTPException('Solución no encontrada')
    format = solution['real_name'].split('.')[-1]
    md, file = dbx.files_download(
        f'/solutions/{solutionid}.{format}')
    return io.BytesIO(file.content), solution['real_name']
