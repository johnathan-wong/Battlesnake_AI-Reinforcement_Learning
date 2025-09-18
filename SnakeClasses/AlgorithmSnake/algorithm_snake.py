from ..base_snake import MySnake
import typing
import collections
import heapq
import math

class AlgorithmSnake(MySnake):
    """
    """
    def move(self, game_state: typing.Dict) -> typing.Dict:
        # Basic Info
        width = game_state['board']['width']
        height = game_state['board']['height']
        snakes = game_state['board']['snakes']
        my_snake = next((snake for snake in snakes if snake["id"] == self.id), None)
        my_head = self._dict_to_tuple(my_snake['body'][0])
        my_id = my_snake['id']
        my_length = len(my_snake['body'])
        longest_length = max(len(snake['body']) for snake in snakes)
        foods = game_state['board']['food']
        
        # Flood-Fill Algorithm call
        '''
        Calculate all the "safe space" from all the movement choice {left, right, up, down}
        '''
        empty_space: typing.Dict[str, int] = {}
        my_head = self._dict_to_tuple(my_snake['body'][0])
        empty_space["left"] = self.__flood_fill_search((my_head[0]-1, my_head[1]), game_state, width, height)
        empty_space["right"] = self.__flood_fill_search((my_head[0]+1, my_head[1]), game_state, width, height)
        empty_space["down"] = self.__flood_fill_search((my_head[0], my_head[1]+1), game_state, width, height)
        empty_space["up"] = self.__flood_fill_search((my_head[0], my_head[1]-1), game_state, width, height)
        result = sorted(empty_space.items(), key=lambda item: item[1], reverse=True)
        # A* Algorithm call
        '''
        Find shortest path to closest food among all snakes
        '''
        food_distance = {self._dict_to_tuple(food): {} for food in foods}
                
        for snake in snakes:
            snake_head = self._dict_to_tuple(snake['body'][0])
            for food in foods:
                food_pos = self._dict_to_tuple(food)
                to_food_path = self.__a_star_search(game_state, snake_head, food_pos)
                if to_food_path:
                    food_distance[food_pos][snake['id']] = len(to_food_path)
        # - Filter Safe Food
        safe_foods = []        
        for food_pos, snake_data in food_distance.items():
            my_path_len = snake_data.get(my_id)
            if my_path_len is None:
                continue
            
            if any(
                (opp_path_len is not None) and
                (opp_path_len < my_path_len or (opp_path_len == my_path_len and len(snake['body']) >= my_length))
                for snake in snakes if snake['id'] != my_snake['id']
                for opp_path_len in [snake_data.get(snake['id'])]
                ):
                continue
            safe_foods.append((food_pos, my_path_len))
            
        # print(result)
        # - Sort Foods and Get Target Path
        safe_foods.sort(key=lambda x: x[1])
        for closest_to_food in safe_foods:
            target_food = closest_to_food[0]
            target_path =  self.__a_star_search(game_state, my_head, target_food)
            target_dir = self._get_direction_from_neighbhor_(target_path[0], target_path[1])
            if empty_space[target_dir] > longest_length:
                return {"move": target_dir} 
            
        # - No Safe path to Food
        best_direction = result[0][0]
        return {"move": best_direction} 
    
    """
    Search Algorithm
    """
    def __flood_fill_search(self,start_pos:typing.Tuple[int, int], game_state: typing.Dict, width: int, height: int) -> int:
        # Basic Info
        # my_snake = next((snake for snake in snakes if snake["id"] == self.id), None)
        opponents = game_state['board']['snakes']
        foods = game_state['board']['food']
        # Variables
        visited = set()
        occupied_space = set()
        # food_space = set()
        queue = collections.deque([start_pos])
        visited.add(start_pos)
        count = 0
        
        # occupied space initialize
        for snake in opponents:
            # Add Body
            for pos in snake["body"][:-1]:
                occupied_space.add(self._dict_to_tuple(pos))

            # Add Tail
            head_pos = self._dict_to_tuple(snake["body"][0])
            for food in foods:
                food_pos = self._dict_to_tuple(food)
                if abs(head_pos[0] - food_pos[0]) + abs(head_pos[1] - food_pos[1]) == 1:
                    tail_pos = self._dict_to_tuple(snake["body"][-1])
                    occupied_space.add(tail_pos)
            
            # Add neighbors of the head
            occupied_space.add((head_pos[0] + 1, head_pos[1]))
            occupied_space.add((head_pos[0] - 1, head_pos[1]))
            occupied_space.add((head_pos[0], head_pos[1] + 1))
            occupied_space.add((head_pos[0], head_pos[1] - 1))      
                    
                
        if start_pos in occupied_space:
            return count
        
        
        while queue:
            cur_pos = queue.popleft()
            neighbors = self._get_neighbors_(cur_pos)
            
            for next_x, next_y in neighbors:
                next_pos = (next_x, next_y)
                # Check is wall
                # Check is occupied
                # Check is visited
                if (0 <= next_x < width and 0 <= next_y < height and
                    next_pos not in occupied_space and
                    next_pos not in visited):
                    
                    visited.add(next_pos)
                    queue.append(next_pos)
                    count += 1
            
        return count
        
    def __a_star_search(self, game_state: typing.Dict, start_pos, goal_pos):
        # Basic Info
        width = game_state['board']['width']
        height = game_state['board']['height']
        snakes = game_state['board']['snakes']
        obstacles = {self._dict_to_tuple(pos) for snake in snakes for pos in snake['body']}
        obstacles.discard(start_pos)
        
        open_heap = []
        open_set = set()
        came_from = {}
        g_score = {(x, y): math.inf for x in range(width) for y in range(height)}
        f_score = {(x, y): math.inf for x in range(width) for y in range(height)}

        g_score[start_pos] = 0
        f_score[start_pos] = g_score[start_pos] + self._manhattan_distance_(start_pos, goal_pos)
        heapq.heappush(open_heap, (f_score[start_pos], start_pos))
        open_set.add(start_pos)
        
        while open_heap:
            _, cur = heapq.heappop(open_heap)
            open_set.remove(cur)
            if cur == goal_pos:
                return self._reconstruct_path_(came_from, cur)
            if cur in obstacles:
                continue
            for neighbor in self._get_neighbors_(cur):
                if not (0 <= neighbor[0] < width and 0 <= neighbor[1] < height):
                    continue
                tentative_gScore = g_score[cur] + 1
                if tentative_gScore < g_score[neighbor]:
                    came_from[neighbor] = cur
                    g_score[neighbor] = tentative_gScore
                    f_score[neighbor] = g_score[neighbor] + self._manhattan_distance_(neighbor, goal_pos)
                    
                    if neighbor not in open_set:
                        heapq.heappush(open_heap, (f_score[neighbor], neighbor))
                        open_set.add(neighbor)
                
        return []
    
    """
    Helper Functions
    """
    def _dict_to_tuple(self, dict_pos: typing.Dict) -> typing.Tuple:
        return (dict_pos["x"], dict_pos["y"])
    
    def _get_neighbors_(self, given_pos: typing.Tuple) -> typing.List[typing.Tuple]:
        x, y = given_pos
        return [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]
    
    def _manhattan_distance_(self, pos1: typing.Tuple[int, int], pos2: typing.Tuple[int, int]) -> int:
        return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])
    
    def _reconstruct_path_(self, came_from, current):
        path = [current]
            
        while current in came_from:
            current = came_from[current]
            path.insert(0, current)
        
        return path
    
    def _get_direction_from_neighbhor_(self, head_pos, neighbor_pos):
        hx, hy = head_pos
        nx, ny = neighbor_pos

        if nx == hx and ny == hy + 1:
            return "up"
        elif nx == hx and ny == hy - 1:
            return "down"
        elif nx == hx - 1 and ny == hy:
            return "left"
        elif nx == hx + 1 and ny == hy:
            return "right"
        else:
            return None  # Not a valid direct neighbor