from app import app, host
from app.controllers.account import bp as bp_account
from app.controllers.user import bp as bp_user
from app.controllers.role import bp as bp_role

app.register_blueprint(bp_account, url_prefix='/api/account')
app.register_blueprint(bp_user, url_prefix='/api/user')
app.register_blueprint(bp_role, url_prefix='/api/role')

if __name__ == '__main__':
    app.run(host, 5000, True)