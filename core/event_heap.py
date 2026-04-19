from scenes.defeat_menu import DefeatMenu
from scenes.victory_menu import VictoryMenu

class EventHeap:
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def _up_heap(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._up_heap(parent)

    def _down_heap(self, index):
        min_index = index
        left = 2 * (index + 1) - 1
        right = 2 * (index + 1)

        n = len(self.heap)
        if left < n and self.heap[left][0] < self.heap[min_index][0]:
            min_index = left
        if right < n and self.heap[right][0] < self.heap[min_index][0]:
            min_index = right

        if min_index != index:
            self.heap[index], self.heap[min_index] = self.heap[min_index], self.heap[index]
            self._down_heap(min_index)

    def push(self, event):
        self.heap.append(event)
        self._up_heap(len(self.heap) - 1)

    def pop(self):
        if self.is_empty():
            return None
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        if not self.is_empty():
            self._down_heap(0)

    def top(self):
        if self.is_empty():
            return None
        return self.heap[0]
    
    def process_events(self, current_frame, scene):
        while True:
            if self.is_empty():
                break

            event_frame, event_type, event_args = self.top()
            if event_frame > current_frame:
                break
            self.pop()

            if event_type == "damage":
                target_enemy, damage = event_args
                target_enemy.current_health -= damage
            
            elif event_type == "spawn":
                path_index, enemy_name = event_args
                scene.spawn_enemy(path_index, enemy_name)

            elif event_type == "defeat":
                scene.game_manager.change_scene(DefeatMenu(scene.game_manager, scene))

            elif event_type == "victory":
                scene.game_manager.change_scene(VictoryMenu(scene.game_manager, scene))