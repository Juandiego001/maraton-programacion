from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.response import ResponseIn, ResponseOut, Responses
from app.schemas.generic import Message
from app.services import response
from app.utils import success_message

bp = APIBlueprint('response', __name__)

@bp.post('/')
@bp.input(ResponseIn)
@bp.output(Message)
@jwt_required()
def create_structure(data):
    try:
        data['updated_by'] = get_jwt()['username']
        response.create_response(data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/<string:responseid>')
@bp.output(ResponseOut)
def get_response_detail(responseid):
    try:
        return ResponseOut().dump(response.get_response_by_id(responseid))
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/')
@bp.output(Responses)
def get_structures():
    try:
        return Responses().dump({'items': response.get_responses()})
    except Exception as ex:
        abort(500, str(ex))

@bp.patch('/<string:responseid>')
@bp.input(ResponseIn)
@bp.output(Message)
@jwt_required()
def update_response(responseid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        response.update_response(responseid, data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

