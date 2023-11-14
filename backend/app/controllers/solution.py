from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.services import solution
from app.schemas.solution import SolutionIn, SolutionOut, Solutions
from app.schemas.generic import Message
from app.utils import success_message


bp = APIBlueprint('solution', __name__)


@bp.post('/')
@bp.input(SolutionIn, location='files')
@bp.output(Message)
@jwt_required()
def create_solution(files_data):
    try:
        files_data['updated_by'] = get_jwt()['username']
        solution.create_solution(files_data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Solutions)
def get_solutions():
    try:
        return Solutions().dump({'items': solution.get_solutions()})
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:solutionid>')
@bp.output(SolutionOut)
def get_solution(solutionid):
    try:
        return solution.get_solution_by_id(solutionid)
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