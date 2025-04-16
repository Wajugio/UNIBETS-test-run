from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required
from auth import auth_bp
from database import init_db

app = Flask(__name__)
app.secret_key = 'super-secret-unibets-key'
app.register_blueprint(auth_bp)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
from database import get_user_by_id  # make sure this is imported


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


init_db()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
