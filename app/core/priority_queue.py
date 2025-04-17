from typing import List, Optional
from app.models.todo_item import TodoItem
import heapq

class PriorityQueue:
    def __init__(self):
        self._items: List[TodoItem] = []
        self._id_counter = 1
        self._priority_set = set()

    def clear_queue(self):
        self._items = []
        self._id_counter = 1
        self._priority_set = set()

    def add_item(self, item: TodoItem) -> TodoItem:
        item.id = self._id_counter
        self._id_counter += 1
        heapq.heappush(self._items, (item.priority, item.id, item))
        self._priority_set.add(item.priority)
        return item

    def get_item(self, item_id: int) -> Optional[TodoItem]:
        for _, _, item in self._items:
            if item.id == item_id:
                return item
        return None

    def delete_item(self, item_id: int) -> bool:
        for i, (_, id, _) in enumerate(self._items):
            if id == item_id:
                priority = self._items[i][0]
                self._items.pop(i)
                heapq.heapify(self._items)
                # Remove priority from set if no other items have it
                if not any(p == priority for p, _, _ in self._items):
                    self._priority_set.remove(priority)
                return True
        return False

    def get_all_items(self) -> List[TodoItem]:
        return [item for _, _, item in sorted(self._items)]

    def get_missing_priorities(self) -> List[int]:
        if not self._priority_set:
            return []
        min_priority = min(self._priority_set)
        max_priority = max(self._priority_set)
        all_priorities = set(range(min_priority, max_priority + 1))
        return sorted(list(all_priorities - self._priority_set)) 