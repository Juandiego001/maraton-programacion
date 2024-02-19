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
    params['file_url'] = f'{solutionid}?v={generate_id()}'
    params['created_at'] = params['updated_at'] = datetime.now()
    params['status'] = True
    created = mongo.db.solutions.insert_one(params)
    if not created:
        raise HTTPException('La solución no fue creada')
    return created


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
                'judgment_status': 1,
                'error': 1,
                'description': 1,
                'status': 1
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
            '$match': filter
        }, {
            '$project': {
                'file_url': 1,
                'real_name': 1,
                'link': 1,
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
    solution = verify_exists([{'_id': ObjectId(solutionid)}])
    if not solution:
        raise HTTPException('Solución no encontrada')
    if 'file' in params:
        params['real_name'] = put_file(params.pop('file'), solutionid)
        params['file_url'] = f'{solutionid}?v={generate_id()}'

    params['updated_at'] = datetime.now()
    updated = mongo.db.solutions.find_one_and_update(
        {'_id': ObjectId(solutionid)}, {'$set': params})
    if not updated:
        raise HTTPException('Solución no encontrada')
    return updated


def download_solution(solutionid: str):
    solution = verify_exists([{'_id': ObjectId(solutionid)}])
    if not solution:
        raise HTTPException('Solución no encontrada')
    format = solution['real_name'].split('.')[-1]
    md, file = dbx.files_download(
        f'/solutions/{solutionid}.{format}')
    return io.BytesIO(file.content), solution['real_name']
