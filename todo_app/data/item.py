class Item:
    def __init__(self, id, name, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_cosmos_db(cls, task):
        return cls(task['_id'], task['name'], task['status'])

    def __eq__(self, other):
        if not isinstance(other, Item):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.id == other.id and self.name == other.name and self.status == other.status