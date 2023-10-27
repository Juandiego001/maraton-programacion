from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.topic import TopicIn, TopicOut, Topics
from app.schemas.generic import Message
from app.services import topic
from app.utils import successfull_message

bp = APIBlueprint('topic', __name__)

@bp.post('/')
@bp.input(TopicIn)
@bp.output(Message)
@jwt_required()
def create_topic(data):
    try:
        data['updated_by'] = get_jwt()['username']
        topic.create_topic(data)
        return successfull_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/<string:topicid>')
@bp.output(TopicOut)
def get_topic_detail(topicid):
    try:
        return TopicOut().dump(topic.get_topic_by_id(topicid))
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

@bp.get('/')
@bp.output(Topics)
def get_topics():
    try:
        return Topics().dump({'items': topic.get_topics()})
    except Exception as ex:
        abort(500, str(ex))

@bp.patch('/<string:topicid>')
@bp.input(TopicIn)
@bp.output(Message)
@jwt_required()
def update_topic(topicid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        topic.update_topic(topicid, data)
        return successfull_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))

