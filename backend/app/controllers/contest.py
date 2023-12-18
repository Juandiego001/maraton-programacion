from werkzeug.exceptions import HTTPException
from flask import send_file
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.contest import ContestIn, ContestOut, Contests, ContestsQuery
from app.schemas.generic import Message
from app.services import contest
from dropbox.exceptions import HttpError
from app.utils import success_message


bp = APIBlueprint('contest', __name__)


@bp.post('/')
@bp.input(ContestIn, location='files')
@bp.output(Message)
@jwt_required()
def create_contest(files_data):
    try:
        files_data['updated_by'] = get_jwt()['username']
        contest.create_contest(files_data)
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
@bp.input(ContestsQuery, location='query')
@bp.output(Contests)
def get_contests(query):
    try:
        return Contests().dump({'items': contest.get_contests(query)})
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:contestid>')
@bp.input(ContestIn, location='files')
@bp.output(Message)
@jwt_required()
def update_contest(contestid, files_data):
    try:
        files_data['updated_by'] = get_jwt()['username']
        contest.update_contest(contestid, files_data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/download/<string:contestid>')
def download_contest(contestid):
    try:
        file_data, real_name = contest.download_contest(contestid)
        return send_file(file_data,
                         as_attachment=True,
                         download_name=real_name)
    except HttpError as ex:
        abort(ex.status_code, ex.body)
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))