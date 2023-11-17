from bson import ObjectId
from flask import send_file
from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.services import material
from app.schemas.material import MaterialIn, MaterialOut, Materials
from app.schemas.generic import Message
from dropbox.exceptions import HttpError
from app.utils import success_message


bp = APIBlueprint('material', __name__)


@bp.post('/')
@bp.input(MaterialIn, location='files')
@bp.output(Message)
@jwt_required()
def create_material(files_data):
    try:
        files_data['userid'] = ObjectId(get_jwt()['_id'])
        files_data['updated_by'] = get_jwt()['username']
        material.create_material(files_data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Materials)
def get_materials():
    try:
        return Materials().dump({'items': material.get_materials()})
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:materialid>')
@bp.output(MaterialOut)
def get_material(materialid):
    try:
        return material.get_material_by_id(materialid)
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:materialid>')
@bp.input(MaterialIn, location='files')
@bp.output(Message)
@jwt_required()
def update_role(materialid, files_data):
    try:
        files_data['updated_by'] = get_jwt()['username']
        material.update_material(materialid, files_data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/download/<string:materialid>')
def download_material(materialid):
    try:
        file_data, real_name = material.download_material(materialid)
        return send_file(file_data,
                         as_attachment=True,
                         download_name=real_name)
    except HttpError as ex:
        abort(ex.status_code, ex.body)
    except HTTPException as ex:
        abort(404, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.delete('/<string:materialid>')
def delete_material(materialid):
    try:
        material.delete_file(materialid)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))
