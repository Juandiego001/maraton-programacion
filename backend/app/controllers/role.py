from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.services import role
from app.schemas.role import RoleIn, RoleOut, Roles
from app.schemas.generic import Message

bp = APIBlueprint('role', __name__)

@bp.post('/')
@bp.input(RoleIn)
@bp.output(Message)
@jwt_required()
def create_role(data):
    try:
        data['updated_by'] = get_jwt()['username']
        role.create_rol(data)
        return {'message': 'Rol creado con éxito'}
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/')
@bp.output(Roles)
def get_roles():
    try:
        return Roles().dump({'items': role.get_roles()})
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/<string:roleid>')
@bp.output(RoleOut)
def get_role(roleid):
    try:
        return RoleOut().dump(role.get_role_by_id(roleid))
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.patch('/<string:roleid>')
@bp.input(RoleIn)
@bp.output(Message)
@jwt_required()
def update_role(roleid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        role.update_role(roleid, data)
        return {'message': 'Rol actualizado exitosamente'}
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))