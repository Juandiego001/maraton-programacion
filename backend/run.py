from app import app, host
from app.controllers.account import bp as bp_account
from app.controllers.user import bp as bp_user

app.register_blueprint(bp_account, url_prefix='/api/account')
app.register_blueprint(bp_user, url_prefix='/api/users')

if __name__ == '__main__':
    app.run(host, 5000, True)