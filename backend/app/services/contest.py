from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId


def create_contest(params: dict):
    params['updated_at'] = datetime.now()
    mongo.db.contests.insert_one(params)


def get_contest_by_id(contestid: str):
    return mongo.db.contests.find_one(ObjectId(contestid))


def get_contests():
    return list(mongo.db.contests.find({}))


def update_contest(contestid, params):
    contest = get_contest_by_id(contestid)
    if not contest:
        raise HTTPException('La competencia no ha sido encontrada')
    
    params['updated_at'] = datetime.now()
    updated = mongo.db.contests.update_one({'_id': ObjectId(contestid)},
                                           {'$set': params})

    if not updated:
        raise HTTPException('La competencia no ha sido encontrada')
    return contest

