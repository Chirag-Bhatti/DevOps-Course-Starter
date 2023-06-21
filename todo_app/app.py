from flask import Flask, redirect, render_template, request
from todo_app.data.cosmosdb_items import add_item, get_items, complete_item
from todo_app.flask_config import Config
from todo_app.view import ViewModel


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    @app.route('/')
    def index():
        items = get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model = item_view_model)

    @app.route('/add-todo-item', methods=['POST'])
    def add_to_do_item():
        name = request.form.get('name')
        add_item(name)
        return redirect('/')

    @app.route('/mark-completed', methods=['POST'])
    def mark_completed():
        id = request.form.get('item_id')
        complete_item(id)
        return redirect('/')   

    return app