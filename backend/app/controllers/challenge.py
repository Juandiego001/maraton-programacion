from werkzeug.exceptions import HTTPException
from apiflask import APIBlueprint, abort
from flask_jwt_extended import get_jwt, jwt_required
from app.schemas.challenge import ChallengeIn, ChallengeOut, Challenges,\
    ChallengeContestOut, ChallengesContest
from app.schemas.generic import Message
from app.services import challenge
from app.utils import success_message


bp = APIBlueprint('challenge', __name__)


@bp.post('/')
@bp.input(ChallengeIn)
@bp.output(Message)
@jwt_required()
def create_challenge(data):
    try:
        data['updated_by'] = get_jwt()['username']
        challenge.create_challenge(data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:challengeid>')
@bp.output(ChallengeContestOut)
def get_challenge_detail(challengeid):
    try:
        return challenge.get_challenge_by_id(challengeid)
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(ChallengesContest)
def get_challenges():
    try:
        return Challenges().dump({'items': challenge.get_challenges()})
    except Exception as ex:
        abort(500, str(ex))


@bp.patch('/<string:challengeid>')
@bp.input(ChallengeIn)
@bp.output(Message)
@jwt_required()
def update_challenge(challengeid, data):
    try:
        data['updated_by'] = get_jwt()['username']
        challenge.update_challenge(challengeid, data)
        return success_message()
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/contest/<string:contestid>')
@bp.output(Challenges)
def get_challenges_by_contest(contestid):
    try:
        test = challenge.get_challenges_by_contest(contestid)
        print('Test: ', test)
        return Challenges().dump(
            {'items': test})
    except HTTPException as ex:
        abort(400, ex.description)
    except Exception as ex:
        abort(500, str(ex))
