from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.difficulty import DifficultyIn, DifficultyOut, Difficulties
from app.schemas.generic import Message
from app.services import difficulty
from app.utils import success_message


bp = APIBlueprint('difficulty', __name__)


@bp.post('/')
@bp.input(DifficultyIn)
@bp.output(Message)
@jwt_required()
def create_difficulty(data):
    try:
        data['updated_by'] = get_jwt()['username']
        difficulty.create_difficulty(data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:difficultyid>')
@bp.output(DifficultyOut)
def get_difficulty_detail(difficultyid):
    try:
        return difficulty.get_difficulty_by_id(difficultyid)
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Difficulties)
def get_difficulties():
    try:
        return Difficulties().dump({'items': difficulty.get_difficulties()})
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:difficultyid>')
@bp.input(DifficultyIn)
@bp.output(Message)
@jwt_required()
def update_difficulty(difficultyid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        difficulty.update_difficulty(difficultyid, data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

