from bson import ObjectId
from flask import send_file
from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.services import solution
from app.schemas.solution import SolutionIn, SolutionOut, Solutions, SolutionsQuery
from app.schemas.generic import Message
from dropbox.exceptions import HttpError
from app.utils import success_message


bp = APIBlueprint('solution', __name__)


@bp.post('/')
@bp.input(SolutionIn, location='files')
@bp.output(Message)
@jwt_required()
def create_solution(files_data):
    try:
        files_data['userid'] = ObjectId(get_jwt()['_id'])
        files_data['updated_by'] = get_jwt()['username']
        solution.create_solution(files_data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.input(SolutionsQuery, location='query')
@bp.output(Solutions)
def get_solutions(query):
    try:
        return Solutions().dump({'items': solution.get_solutions(query)})
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:solutionid>')
@bp.output(SolutionOut)
def get_solution(solutionid):
    try:
        sol = solution.get_solution_by_id(solutionid)
        print('sol: ', sol)
        return sol
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:solutionid>')
@bp.input(SolutionIn, location='files')
@bp.output(Message)
@jwt_required()
def update_role(solutionid, files_data):
    try:
        files_data['updated_by'] = get_jwt()['username']
        solution.update_solution(solutionid, files_data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/download/<string:solutionid>')
def download_solution(solutionid):
    try:
        file_data, real_name = solution.download_solution(solutionid)
        return send_file(file_data,
                         as_attachment=True,
                         download_name=real_name)
    except HttpError as ex:
        abort(ex.status_code, ex.body)
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))