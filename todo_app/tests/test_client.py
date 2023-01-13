import os
from dotenv import find_dotenv, load_dotenv
import pytest
import requests

from todo_app import app


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

class StubResponse():
    def __init__(self, fake_response_data, status_code):
        self.fake_response_data = fake_response_data
        self.status_code = status_code

    def json(self):
        return self.fake_response_data

def stub(url, params={}):
    test_board_id = os.environ.get('BOARD_ID')
    fake_response_data = None
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{'id': '456', 'name': 'Test card'}]
        }]
        status_code = 200
        stubbedResponse =  StubResponse(fake_response_data, status_code)
        return stubbedResponse

    raise Exception(f'Integration test did not expect URL "{url}"')

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', stub)

    response = client.get('/')

    assert response.status_code == 200
    assert '<li>456 - To Do - Test card</li>' in response.data.decode()