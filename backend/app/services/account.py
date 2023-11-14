import json
from werkzeug.exceptions import HTTPException
from threading import Timer
from flask import render_template
from app import app, smtp_config, mongo
from app.utils import send_mail
from bson import json_util, ObjectId


def login(user_data: dict):
    user = mongo.db.users.find_one(
        {'username': user_data['username'], 
         'password': user_data['password']})
    if not user:
        raise HTTPException('Usuario o contraseña incorrectos')
    else:
        return user


def get_user_by_id(user_id: str):
    return mongo.db.users.find_one(ObjectId(user_id))


def get_user_by_email(email: str):
    return mongo.db.users.find_one({'email': email})


def get_user_permissions(username: str, permission: str):
    return list(mongo.db.user_roles.aggregate([
        {
            '$lookup': {
                'from': 'permissions', 
                'localField': 'roleid', 
                'foreignField': 'roleid', 
                'let': {
                    f'{permission}': f'${permission}'
                },
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'modules', 
                            'localField': 'moduleid', 
                            'foreignField': '_id', 
                            'as': 'modules'
                        }
                    }, {
                        '$unwind': {
                            'path': '$modules'
                        }
                    }, {
                        '$match': {
                            '$expr': {
                                '$eq': [
                                    f'${permission}', True
                                ]
                            }
                        }
                    }, {
                        '$addFields': {
                            'subject': '$modules.name',
                            'action': f'${permission}',
                        }
                    }
                ], 
                'as': 'permissions'
            }
        }, {
          '$unwind': {
            'path': '$permissions'
          }
        }, {
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
            '$match': {
                '$expr': {
                    '$eq': [
                        '$user.username', username
                    ]
                }
            }
        }, {
          '$group': {
            '_id': '$permissions.subject',
            'actions': { '$push': '$permissions.action' }
          }
        },  {
          '$addFields': {
            'action': {
              '$cond': {
                'if': {
                  '$eq': [{'$anyElementTrue': ['$actions']}, True],
                },
                'then': f'{permission}',
                'else': {}
              },
            }
          }
        }, {
            '$project': {
                '_id': 0, 
                'action': 1,
                'subject': '$_id'
            }
        }
    ]))


def request_reset_password(email: str):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException('User not found')
    userid = json.loads(json_util.dumps(user))
    link = f'{app.config["URL_PASSWORD_RESET"]}/{userid["_id"]["$oid"]}'
    message = render_template(
        'mail/reset-password.html',
        link=link)
    with app.app_context():
        t = Timer(0, send_mail, args=(smtp_config,
                                      'Reestablece tu contraseña',
                                      email, message,))
        t.start()


def set_password(userid: str, new_password: str):
    updated = mongo.db.users.find_one_and_update(
        {'_id': ObjectId(userid)},
        {'$set': {'password': new_password}})
    if not updated:
        raise HTTPException('User not found')


def change_password(userid: str, data: dict):
    updated = mongo.db.users.find_one_and_update(
        {'_id': ObjectId(userid), 'password': data['current_password']},
        {'$set': {'password': data['new_password']}})
    if not updated:
        raise HTTPException('Current password doesnt match')
