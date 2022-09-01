from flask import Flask, redirect, render_template, request
from todo_app.data.session_items import add_item, complete_item, get_items

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    to_do_items = get_items()
    return render_template('index.html', toDoItems = to_do_items)

@app.route('/add-todo-item', methods=['POST'])
def add_to_do_item():
    title = request.form.get('title')
    add_item(title)
    return redirect('/')

@app.route('/mark-completed', methods=['POST'])
def mark_completed():
    id = request.form.get('item_id')
    complete_item(id)
    return redirect('/')