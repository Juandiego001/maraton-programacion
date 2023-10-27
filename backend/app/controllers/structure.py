from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.structure import StructureIn, StructureOut, Structures
from app.schemas.generic import Message
from app.services import structure
from app.utils import successfull_message

bp = APIBlueprint('structure', __name__)

@bp.post('/')
@bp.input(StructureIn)
@bp.output(Message)
@jwt_required()
def create_structure(data):
    try:
        data['updated_by'] = get_jwt()['username']
        structure.create_structure(data)
        return successfull_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/<string:structureid>')
@bp.output(StructureOut)
def get_structure_detail(structureid):
    try:
        return StructureOut().dump(structure.get_structure_by_id(structureid))
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/')
@bp.output(Structures)
def get_structures():
    try:
        return Structures().dump({'items': structure.get_structures()})
    except Exception as ex:
        abort(500, str(ex))

@bp.patch('/<string:structreid>')
@bp.input(StructureIn)
@bp.output(Message)
@jwt_required()
def update_structure(structureid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        structure.update_structure(structureid, data)
        return successfull_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

