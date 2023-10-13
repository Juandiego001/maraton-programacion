from datetime import datetime
from werkzeug.exceptions import HTTPException
from app import mongo
from bson import ObjectId

def create_rol_permission(params: dict):
    pass

def create_user(params: dict):
    user = verify_if_user_exists([
        {'username': params['username']},
        {'email': params['email']},
        {'document': params['document']},
    ])
    if user:
        raise HTTPException('El usuario ya existe')
    params['status'] = 'PENDING'
    params['updated_at'] = datetime.now()
    roleid = mongo.db.roles.find_one({'name': 'Administrador'})['_id']
    userid = mongo.db.users.insert_one(params).inserted_id
    return create_rol_permission({
        'userid': userid,
        'profileid': roleid
    })    

def get_user_by_id(userid: str):
    user = mongo.db.usuario.find_one(ObjectId(userid))
    if not user:
        raise HTTPException('User not found')
    return user

def get_users():
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

def verify_if_user_exists(data: list):
    return mongo.db.users.find_one({'$or': data})

def update_user(userid, data):
    userid = ObjectId(userid)
    user = mongo.db.users.find_one({'_id': userid})
    if not user:
        raise HTTPException('User was not found')
    
    verify_data = [
        {'username': data['username']\
         if user['username'] != data['username'] else ''},
        {'email': data['email']\
         if user['email'] != data['email'] else ''},
        {'document': data['document']\
         if user['document'] != data['document'] else ''}
    ]

    if verify_if_user_exists(verify_data):
        raise HTTPException('User already registered')
    
    data['updated_at'] = datetime.now()

    # Se evita que al actualizar se reinicie la contraseña de manera
    # no deseada
    if data['password'] == '':
        data.pop('password')

    updated = mongo.db.users.update_one({'_id': userid}, {'$set': data})

    if not updated:
        raise HTTPException('User not found')
    return user

