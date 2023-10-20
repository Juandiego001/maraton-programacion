from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.permission import PermissionIn, PermissionOut
from app.schemas.generic import Message
from app.services import permission

bp = APIBlueprint('permission', __name__)

@bp.post('/')
@bp.input(PermissionIn)
@bp.output(Message)
@jwt_required()
def create_permission(data):
    try:
        data['updated_by'] = get_jwt()['username']
        permission.create_permission(data)
    except Exception as ex:
        abort(500, str(ex))

@bp.patch('/<string:permissionid>')
@bp.input(PermissionIn)
@bp.output(PermissionOut)
def update_permission(permissionid):
    try:
        permission.update_permission(permissionid, )
    except Exception as ex:
        abort(500, str(ex))