from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.language import LanguageIn, LanguageOut, Languages
from app.schemas.generic import Message
from app.services import language
from app.utils import success_message


bp = APIBlueprint('language', __name__)


@bp.post('/')
@bp.input(LanguageIn)
@bp.output(Message)
@jwt_required()
def create_language(data):
    try:
        data['updated_by'] = get_jwt()['username']
        language.create_language(data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:languageid>')
@bp.output(LanguageOut)
def get_language_detail(languageid):
    try:
        return language.get_language_by_id(languageid)
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Languages)
def get_topics():
    try:
        return Languages().dump({'items': language.get_languages()})
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:languageid>')
@bp.input(LanguageIn)
@bp.output(Message)
@jwt_required()
def update_language(languageid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        language.update_language(languageid, data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

