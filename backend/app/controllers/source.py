from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.source import SourceIn, SourceOut, Sources
from app.schemas.generic import Message
from app.services import source
from app.utils import success_message


bp = APIBlueprint('source', __name__)


@bp.post('/')
@bp.input(SourceIn)
@bp.output(Message)
@jwt_required()
def create_source(data):
    try:
        data['updated_by'] = get_jwt()['username']
        source.create_source(data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:sourceid>')
@bp.output(SourceOut)
def get_source_detail(sourceid):
    try:
        return source.get_source_by_id(sourceid)
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Sources)
def get_sources():
    try:
        return Sources().dump({'items': source.get_sources_for_languages()})
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/languages/<string:challengeid>')
@bp.output(Sources)
def get_sources_for_languages(challengeid):
    try:
        return Sources().dump({'items': source.get_sources_for_languages(challengeid)})
    except Exception as ex:
        abort(500, str(ex))