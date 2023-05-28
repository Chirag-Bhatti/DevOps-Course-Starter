import mongomock
import pytest
from dotenv import find_dotenv, load_dotenv
from todo_app import app
from todo_app.data.cosmosdb_items import add_item, connect_to_task_collection


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        
        with test_app.test_client() as client:
            yield client

def test_index_page(monkeypatch, client):
    id = add_item("Test Task")
    response = client.get('/')

    assert response.status_code == 200
    assert f'<li>{id} - To Do - Test Task</li>' in response.data.decode()