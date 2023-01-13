import os
import requests
from todo_app.data.item import Item

def get_auth_query_params():
    return {
        'key': os.getenv('API_KEY'), 
        'token': os.getenv('TOKEN')
    }

def get_items():
    """
    Fetches all the cards on the To Do list of the Trello Board

    Returns:
        list: The open cards from the Trello board in the form of an Item
    """
    customQueryParams = get_auth_query_params()
    customQueryParams['cards'] = 'open'

    response = requests.get(
        os.getenv('API_BASE_URL') + '/1/boards/{}/lists'.format(os.getenv('BOARD_ID')), 
        params=customQueryParams
    )

    if (response.status_code == requests.status_codes.codes.ok): 
        lists = response.json()
        items = []
        for list in lists:
            for card in list['cards']:
                item = Item.from_trello_card(card, list)
                items.append(item)
        return items


def add_item(title):
    """
    Adds a new card to the To Do list of the Trello Board

    Args:
        title: The title of the card.

    Returns:
        item: The newly added Trello card's details
    """
    response = requests.post(
        os.getenv('API_BASE_URL') + '/1/cards', 
        params=get_auth_query_params(), 
        data={'name': title, 'idList': os.getenv('TO_DO_LIST_ID')}
    )

    if (response.status_code == requests.status_codes.codes.ok):
        newCard = response.json()
        return newCard


def complete_item(id):
    """
    Moves a card from the To Do list to the Done List of the Trello Board

    Args:
        id: The Trello card id to be completed
    
    Returns:
        item: The completed Trello card's details
    """
    customQueryParams = get_auth_query_params().copy()
    customQueryParams['idList'] = os.getenv('DONE_LIST_ID')

    response = requests.put(
        os.getenv('API_BASE_URL') + '/1/cards/{}'.format(id), 
        params=customQueryParams
    )

    if (response.status_code == requests.status_codes.codes.ok):
        completedCard = response.json()
        return completedCard