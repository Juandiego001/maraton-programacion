from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.user import UserIn, UserOut, Users
from app.schemas.generic import Message
from app.services import user

bp = APIBlueprint('user', __name__)

@bp.post('/')
@bp.input(UserIn)
@bp.output(Message)
@jwt_required()
def create_user(data):
    try:
        data['updated_by'] = get_jwt()['username']
        user.create_user(data)
        return {'message': 'User created successfully'}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/<string:userid>')
@bp.output(UserOut)
def get_user_detail(userid):
    try:
        return user.get_admin_by_id(userid)
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/')
@bp.output(Users)
def get_users():
    try:
        return Users().dump({'items': user.get_admins()})
    except Exception as ex:
        abort(500, str(ex))

@bp.patch('/<string:userid>')
@bp.input(UserIn)
@bp.output(Message)
@jwt_required()
def update_user(userid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        user.update_admin(userid, data)
        return {'message': 'User updated successfully'}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

