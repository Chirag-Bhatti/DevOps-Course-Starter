import os
import requests
from todo_app.data.item import Item


API_BASE_URL = 'https://api.trello.com'

BOARD_ID = os.getenv('BOARD_ID')

AUTH_QUERY_PARMS = {
    'key': os.getenv('API_KEY'), 
    'token': os.getenv('TOKEN')
}

def get_list_id(listname):
    response = requests.get(API_BASE_URL + '/1/boards/{}/lists'.format(BOARD_ID), params=AUTH_QUERY_PARMS)
    if (response.status_code == requests.status_codes.codes.ok): 
        lists = response.json()
        for list in lists:
            if (list['name'] == listname):
                return list['id']

TO_DO_LIST_ID = get_list_id('To Do')
DONE_LIST_ID = get_list_id('Done')


def get_items():
    """
    Fetches all the cards on the To Do list of the Trello Board

    Returns:
        list: The open cards from the Trello board in the form of an Item
    """
    customQueryParams = AUTH_QUERY_PARMS.copy()
    customQueryParams['cards'] = 'open'

    response = requests.get(
        API_BASE_URL + '/1/boards/{}/lists'.format(BOARD_ID), 
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
        API_BASE_URL + '/1/cards', 
        params=AUTH_QUERY_PARMS, 
        data={'name': title, 'idList': TO_DO_LIST_ID}
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
    customQueryParams = AUTH_QUERY_PARMS.copy()
    customQueryParams['idList'] = DONE_LIST_ID

    response = requests.put(
        API_BASE_URL + '/1/cards/{}'.format(id), 
        params=customQueryParams
    )

    if (response.status_code == requests.status_codes.codes.ok):
        completedCard = response.json()
        return completedCard