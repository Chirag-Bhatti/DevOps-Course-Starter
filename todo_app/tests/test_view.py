import pytest

from todo_app.data.item import Item
from todo_app.view import ViewModel

@pytest.fixture
def test_items():
    todo_item = Item("todo_id", "todo_name", "To Do")
    doing_item = Item("doing_id", "doing_name", "Doing")
    done_item = Item("done_id", "done_name", "Done")

    return [todo_item, doing_item, done_item]

def test_to_do_items(test_items):
    # Arrange
    view_model = ViewModel(test_items)

    # Act
    view_todo = view_model.todo_items

    # Asert
    assert len(view_todo) == 1
    assert view_todo[0].id == "todo_id"
    assert view_todo[0].name == "todo_name"
    assert view_todo[0].status == "To Do"

def test_doing_items(test_items):
    # Arrange
    view_model = ViewModel(test_items)
    
    # Act
    view_doing = view_model.doing_items

    # Assert
    assert len(view_doing) == 1
    assert view_doing[0].id == "doing_id"
    assert view_doing[0].name == "doing_name"
    assert view_doing[0].status == "Doing"

def test_done_items(test_items):
    # Arrange
    view_model = ViewModel(test_items)

    # Act
    view_done  = view_model.done_items

    # Assert
    assert len(view_done) == 1
    assert view_done[0].id == "done_id"
    assert view_done[0].name == "done_name"
    assert view_done[0].status == "Done"