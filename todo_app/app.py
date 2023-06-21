import os
import requests
from flask import Flask, abort, redirect, render_template, request
from flask_login import LoginManager, current_user, login_required, login_user
from functools import wraps
from todo_app.data.cosmosdb_items import add_item, get_items, complete_item
from todo_app.data.user import User
from todo_app.flask_config import Config
from todo_app.view import ViewModel

def get_access_token_query_params():
    return {
        'client_id' : os.getenv('CLIENT_ID'),
        'client_secret' : os.getenv('CLIENT_SECRET')
    }

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    login_disabled = os.getenv('LOGIN_DISABLED') == 'True'
    app.config['LOGIN_DISABLED'] = login_disabled

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(f"https://github.com/login/oauth/authorize?client_id={os.getenv('CLIENT_ID')}", code=302)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    user_roles = {
        'None' : 'reader', # for any user not actually logged in (i.e. anonymous users) are given reader roles unless login has been disabled
        '109098469' : 'writer'
    }

    def get_current_user_role():
        if (login_disabled):
            return 'writer'
        return user_roles.get(current_user.id)

    def check_user_role_is_writer(func):
        @wraps(func)
        def check_user_role(*args, **kwargs):
            current_user_role = get_current_user_role()
            if (current_user_role == 'writer'):
                return func(*args, **kwargs)
            else: 
                return abort(401)
        return check_user_role
    
    @app.route('/')
    @login_required
    def index():
        items = get_items()
        item_view_model = ViewModel(items)
        current_user_role = get_current_user_role()
        return render_template('index.html', user_role = current_user_role, view_model = item_view_model)

    @app.route('/add-todo-item', methods=['POST'], endpoint='func1')
    @login_required
    @check_user_role_is_writer
    def add_to_do_item():
        name = request.form.get('name')
        add_item(name)
        return redirect('/')

    @app.route('/mark-completed', methods=['POST'], endpoint='func2')
    @login_required
    @check_user_role_is_writer
    def mark_completed():
        id = request.form.get('item_id')
        complete_item(id)
        return redirect('/')

    @app.route('/login/callback')
    def login_callback():
        code = request.args.get('code')

        access_token_query_params = get_access_token_query_params()
        access_token_query_params['code'] = code
        accept_header = {'Accept': 'application/json'}

        access_token_response = requests.post(
            'https://github.com/login/oauth/access_token', 
            params = access_token_query_params,
            headers = accept_header
        )

        access_token_response_json = access_token_response.json()
        access_token = access_token_response_json['access_token']
        authorization_header = {'Authorization' : f'Bearer {access_token}'}
        
        user_info_response = requests.get(
            'https://api.github.com/user',
            headers = authorization_header
        )

        user_info_response_json = user_info_response.json()
        user_id = user_info_response_json['id']
        user = User(user_id)
        logged_in_user = login_user(user)

        if (logged_in_user):
            return redirect('/')
        return abort(500)

    return app