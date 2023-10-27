from app import app, host
from app.controllers.account import bp as bp_account
from app.controllers.user import bp as bp_user
from app.controllers.role import bp as bp_role
from app.controllers.topic import bp as bp_topic
from app.controllers.structure import bp as bp_structure
from app.controllers.contest import bp as bp_contest
from app.controllers.challenge import bp as bp_challenge

app.register_blueprint(bp_account, url_prefix='/api/account')
app.register_blueprint(bp_user, url_prefix='/api/user')
app.register_blueprint(bp_role, url_prefix='/api/role')
app.register_blueprint(bp_topic, url_prefix='/api/topic')
app.register_blueprint(bp_structure, url_prefix='/api/structure')
app.register_blueprint(bp_contest, url_prefix='/api/contest')
app.register_blueprint(bp_challenge, url_prefix='/api/challenge')

if __name__ == '__main__':
    app.run(host, 5000, True)