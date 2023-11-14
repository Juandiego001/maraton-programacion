from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.services import permission
from app.schemas.permission import PermissionIn, PermissionInCreate, Permissions
from app.schemas.generic import Message
from app.utils import success_message


bp = APIBlueprint('permission', __name__)


@bp.post('/')
@bp.input(PermissionInCreate)
@bp.output(Message)
@jwt_required()
def create_permission(data):
    try:
        permission.create_permission(data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:permissionid>')
@bp.input(PermissionIn)
@bp.output(Message)
@jwt_required()
def update_permission(permissionid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        permission.update_permission(permissionid, data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:roleid>')
@bp.output(Permissions)
def get_permissions(roleid):
    try:
        return Permissions().dump(
            {'items': permission.get_permissions_by_role(roleid)})
    except Exception as ex:
        abort(500, str(ex))