class ViewModel:
    def __init__(self, items):
        self._items = items
    
    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        return self.__filter_items_by_status("To Do")

    @property
    def doing_items(self):
        return self.__filter_items_by_status("Doing")
    
    @property
    def done_items(self):
        return self.__filter_items_by_status("Done")

    def __filter_items_by_status(self, status):
        filtered_items = []
        for item in self._items:
            if(item.status == status):
                filtered_items.append(item)
        return filtered_items    