import pytest

from todo_app.data.item import Item
from todo_app.view import ViewModel

@pytest.fixture
def test_items():
    todo_item = Item("todo_id", "todo_name", "To Do")
    doing_item = Item("doing_id", "doing_name", "Doing")
    done_item = Item("done_id", "done_name", "Done")

    return [todo_item, doing_item, done_item]

def test_viewmodel_returns_all_todo_items(test_items):
    # Arrange
    view_model = ViewModel(test_items)

    # Act
    view_model_todo = view_model.todo_items

    # Asert
    assert len(view_model_todo) == 1
    assert Item.__eq__(view_model_todo[0], test_items[0])

def test_viewmodel_returns_all_doing_items(test_items):
    # Arrange
    view_model = ViewModel(test_items)
    
    # Act
    view_model_doing = view_model.doing_items

    # Assert
    assert len(view_model_doing) == 1
    assert Item.__eq__(view_model_doing[0], test_items[1])

def test_viewmodel_returns_all_done_items(test_items):
    # Arrange
    view_model = ViewModel(test_items)

    # Act
    view_model_done  = view_model.done_items

    # Assert
    assert len(view_model_done) == 1
    assert Item.__eq__(view_model_done[0], test_items[2])