from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId

def create_user_roles(params: list):
    return mongo.db.user_roles.insert_many(params)

def create_user(params: dict):
    user = verify_if_user_exists([
        {'username': params['username']},
        {'email': params['email']},
    ])
    if user:
        raise HTTPException('El usuario ya existe')
    params['status'] = 'PENDING'
    params['updated_at'] = datetime.now()

    roles = []
    if 'roles' in params:
        roles = params.pop('roles')

    user_id = mongo.db.users.insert_one(params).inserted_id
    user_roles = []
    for role_id in roles:
        if not mongo.db.roles.find_one(ObjectId(role_id)):
            raise HTTPException('Hay roles asociados que no existen')
        user_roles.append({'user_id': user_id, 'role_id': ObjectId(role_id)})
    
    if len(user_roles):
        create_user_roles(user_roles)

def get_user_by_id(userid: str):
    user = mongo.db.users.aggregate([
        {
            '$lookup': {
                'from': 'user_roles', 
                'localField': '_id', 
                'foreignField': 'user_id', 
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'roles', 
                            'localField': 'role_id', 
                            'foreignField': '_id', 
                            'as': 'roles'
                        }
                    }, {
                        '$unwind': {
                            'path': '$roles'
                        }
                    }, {
                        '$project': {
                            'name': '$roles.name', 
                            '_id': '$roles._id'
                        }
                    }
                ], 
                'as': 'user_roles'
            }
        }, {
            '$match': {
                '$expr': {
                    '$eq': [
                        '$_id', ObjectId(userid)
                    ]
                }
            }
        }, {
            '$project': {
                'name': 1, 
                'username': 1, 
                'status': 1, 
                'email': 1, 
                'roles': '$user_roles'
            }
        }]).try_next()
    if not user:
        raise HTTPException('User not found')
    return user

def get_users():
    return list(mongo.db.users.aggregate([
        {
            '$lookup': {
                'from': 'user_roles', 
                'localField': '_id', 
                'foreignField': 'user_id', 
                'pipeline': [
                    {
                        '$lookup': {
                            'from': 'roles', 
                            'localField': 'role_id', 
                            'foreignField': '_id', 
                            'as': 'roles'
                        }
                    }, {
                        '$unwind': {
                            'path': '$roles'
                        }
                    }, {
                        '$project': {
                            'name': '$roles.name', 
                            '_id': '$roles._id'
                        }
                    }
                ], 
                'as': 'user_roles'
            }
        }, {
            '$project': {
                'name': 1, 
                'username': 1, 
                'status': 1, 
                'email': 1, 
                'roles': '$user_roles'
            }
        }
    ]))

def get_users2():
    return list(mongo.db.role_permissions.aggregate(
        [{
            '$lookup': {
                'from': 'perfil', 
                'localField': 'profileid', 
                'foreignField': '_id', 
                'as': 'profile'
            }
        }, {
            '$unwind': {
                'path': '$profile'
            }
        }, {
            '$lookup': {
                'from': 'usuario', 
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
                'profile.name': 'Administrador'
            },
        }, {
            '$project': {
                '_id': '$user._id',
                'name': '$user.name',
                'lastname': '$user.lastname',
                'document': '$user.document',
                'username': '$user.username',
                'email': '$user.email',
                'status': '$user.status',
                'updated_by': '$user.updated_by',
                'updated_at': '$user.updated_at',
            }
        }]))

def verify_if_user_exists(params: list):
    return mongo.db.users.find_one({'$or': params})

def update_user(userid, params):
    userid = ObjectId(userid)
    user = mongo.db.users.find_one({'_id': userid})
    if not user:
        raise HTTPException('User was not found')
    
    verify_data = []
    if 'username' in params:
        verify_data.append({'username': params['username']})
    if 'email' in params:
        verify_data.append({'email': params['email']})

    if len(verify_data) and verify_if_user_exists(verify_data):
        raise HTTPException('User already registered')
    
    params['updated_at'] = datetime.now()

    # Se evita que al actualizar se reinicie la contraseña de manera
    # no deseada
    if 'password' in params and params['password'] == '':
        params.pop('password')

    updated = mongo.db.users.update_one({'_id': userid}, {'$set': params})

    if not updated:
        raise HTTPException('User not found')
    return user

