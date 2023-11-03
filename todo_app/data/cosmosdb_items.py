import logging
import pymongo
import os
from bson.objectid import ObjectId
from todo_app.data.item import Item

app_logger = logging.getLogger("todo_app.app")

def connect_to_task_collection():
    try:
        app_logger.debug("Attempting to connect to the DB")
        client = pymongo.MongoClient(os.getenv('CONNECTION_STRING'))
        db_name = os.getenv('DB_NAME')
        db = client[f'{db_name}']
        task_collection = db['tasks']
        app_logger.debug("Successfully got the tasks from the DB")
        return task_collection
    except:
        app_logger.critical("Could not connect to the DB")

def get_items():
    """
    Fetches all the cards in the Cosmos DB

    Returns:
        list: The tasks in the Cosmos DB in the form of an Item
    """
    task_collection = connect_to_task_collection()

    tasks = task_collection.find()
    items = []
    for task in tasks:
        item = Item.from_cosmos_db(task)
        items.append(item)
    return items


def add_item(title):
    """
    Adds a new card to the Cosmos DB

    Args:
        title: The title of the card.

    Returns:
        inserted_task_id: The newly added card's details
    """
    task_collection = connect_to_task_collection()

    task = {"name" : title, "status" : "To Do"}

    inserted_task = task_collection.insert_one(task)
    return inserted_task.inserted_id


def complete_item(id):
    """
    Updates the status of a card from 'To Do' to 'Done'

    Args:
        id: The id of the task in the Cosmos DB to be completed
    
    Returns:
        modified_count: The number of tasks that were modified
    """
    task_collection = connect_to_task_collection()

    updated_task = task_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": "Done"}})
    return updated_task.modified_count