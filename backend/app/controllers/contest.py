from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.contest import ContestIn, ContestOut, Contests
from app.schemas.generic import Message
from app.services import contest
from app.utils import success_message


bp = APIBlueprint('contest', __name__)


@bp.post('/')
@bp.input(ContestIn)
@bp.output(Message)
@jwt_required()
def create_contest(data):
    try:
        data['updated_by'] = get_jwt()['username']
        contest.create_contest(data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:contestid>')
@bp.output(ContestOut)
def get_contest_detail(contestid):
    try:
        return ContestOut().dump(contest.get_contest_by_id(contestid))
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Contests)
def get_contests():
    try:
        return Contests().dump({'items': contest.get_contests()})
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:contestid>')
@bp.input(ContestIn)
@bp.output(Message)
@jwt_required()
def update_contest(contestid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        contest.update_contest(contestid, data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

