import numpy as np
import random

class BattlesnakeEngine:
    metadata = {"render.modes": ["human"]}
    
    def __init__(self, width, height, num_snakes):
        super().__init__()
        self.width = width
        self.height = height
        self.turn = 1
        self.done = False
        state = self.reset(num_snakes)

    def reset(self, num_snakes):

        self.turn = 1
        self.done = False
        self._intit_game_state()
        self._spawn_snakes(num_snakes)
        self._spawn_food()
        # self.render()
        
        return self._get_game_state()

    def step(self, actions: dict):
        """
        actions: dict {snake_id: action}
        - action ∈ {"up", "down", "left", "right"}
        """

        if self.done:
            print(f"Turn: {self.turn}")
            print(f"Survived Snake: {self.snakes}")
            return self._get_game_state()

        self.turn += 1
        # 1. Snakes Action
        for id, action in actions.items():
            if id in self.snakes:
                self._move(id, action)
                self._handle_death(id)
        # 2. handle food
        self._handle_food(0.1)

        
        # self.render()
        if len(self.snakes) <= 1:
            print(f"Turn: {self.turn}")
            print(f"Survived Snake: {self.snakes}")
            self.done = True

        return self._get_game_state()


    def render(self):
        symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        grid = np.full((self.height, self.width), ".", dtype=str)
        foods = self.state["board"]["food"]
        for i, snake in self.snakes.items():
            head_x, head_y = snake["body"][0]["x"], snake["body"][0]["y"]
            grid[head_y, head_x] = symbols[i % len(symbols)]  # head = uppercase

            for body in snake["body"][1:]:
                x, y = body["x"], body["y"]
                grid[y, x] = symbols[i % len(symbols)].lower()  #

        for food in foods:
            x, y = food['x'], food['y']
            grid[y, x] = "@"
        
        print(f"Turn {self.turn}:")
        print("\n".join(" ".join(row) for row in grid))
        print()
        
    # Initialization
    def _intit_game_state(self):
        game_state = {
            "game": {
                "id": "local-game",
                # "ruleset": {
                #     "name": self.mode,
                #     "version": "cli",
                #     "settings": {
                #         "foodSpawnChance": self.food_spawn_chance,
                #         "minimumFood": self.min_food,
                #         "hazardDamagePerTurn": self.hazard_damage,
                #         "hazardMap": "",
                #         "hazardMapAuthor": "",
                #         "royale": {"shrinkEveryNTurns": self.shrink_turns},
                #         "squad": {
                #             "allowBodyCollisions": False,
                #             "sharedElimination": False,
                #             "sharedHealth": False,
                #             "sharedLength": False,
                #         },
                #     },
                # },
                "map": "standard",
                "timeout": 500,
                "source": "",
            },
            "turn": self.turn,
            "board": {
                "height": self.height,
                "width": self.width,
                "snakes": [],
                "food": [],
                "hazards": [],
            },
        }
        
        self.state = game_state
        
    def _spawn_snakes(self, num_snakes, length=3):        
        self.snakes = {}
        for i in range(num_snakes):
            # random starting head
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            body = [{'x': x, 'y': y} for _ in range(length)]

            snake = {
                "id": i,
                "body": body,
                "health": 100,
                "alive": True
            }
            self.snakes[i] = snake

    def _spawn_food(self):        
        occupied = {pos_to_tuple(pos) for _, snake in self.snakes.items() for pos in snake["body"]}
        occupied.update([pos_to_tuple(food) for food in self.state["board"]["food"]])
        
        while True:
            pos = (random.randint(0, self.width-1), random.randint(0, self.height-1))
            if pos not in occupied:
                self.state["board"]["food"].append(tuple_to_pos(pos))
                break

    def _get_game_state(self):
        self.state["turn"] = self.turn
        self.state["board"]["snakes"] = list(self.snakes.values())
        return self.state

    # Game Logics
    def _move(self, id, action):
        snake_bodies = self.snakes[id]["body"]
        snake_head = snake_bodies[0]
        foods = self.state["board"]["food"]
        
        dir_to_move = {
            'up' : (0, -1),    # Up
            'down' : (0, 1),     # Down
            'left' : (-1, 0),    # Left
            'right' : (1, 0)      # Right
        }
        
        dx, dy = dir_to_move[action]
        new_head = {'x': snake_head['x'] + dx, 'y': snake_head['y'] + dy}
        snake_bodies.insert(0, new_head)
        
        # Tail Logic
        if new_head not in foods:
            snake_bodies.pop()
            self._handle_health(id, -1)
        else:
            self.snakes[id]["health"] = 100
            self._handle_health(id, 100)
        self.snakes[id]["body"] = snake_bodies

    def _handle_food(self, chance_percentage):
        # Remove Eaten
        occupied = {pos_to_tuple(pos) for _, snake in self.snakes.items() for pos in snake["body"]}
        foods = [food for food in self.state["board"]["food"] if pos_to_tuple(food) not in occupied]
        self.state["board"]["food"] = foods
        # Spawn Food Logic
        if len(foods) == 0 or random.random() < chance_percentage:
            self._spawn_food()

    def _handle_death(self, id):
        occupied_body = {pos_to_tuple(pos) for _, snake in self.snakes.items() for pos in snake["body"][1:]}
        heads = {id: pos_to_tuple(snake["body"][0]) for id, snake in self.snakes.items()}
        target_head = pos_to_tuple(self.snakes[id]["body"][0])
        
        if target_head not in occupied_body:
            same_cell_snakes = [sid for sid, head in heads.items() if head == target_head]
            if len(same_cell_snakes) > 1:
                length = {sid: len(self.snakes[sid]["body"]) for sid in same_cell_snakes}
                max_len = max(length.values())
                
                strongest = [sid for sid in same_cell_snakes if len(self.snakes[sid]["body"]) == max_len]
                
                if len(strongest) == 1:
                    # Only Strogest lives
                    disqualified = [sid for sid in same_cell_snakes if sid not in strongest]
                    for sid in disqualified:
                        del self.snakes[sid]
                else:
                    # Tie -> All Collided Snake Dies
                    for sid in same_cell_snakes:
                        del self.snakes[sid]
        if target_head in occupied_body or self._is_outofbound(target_head):
            # Wall/Body Collision
            del self.snakes[id]
        
         
        if len(self.snakes) <= 1:
            # End game Logic
            self.done = True
    
    def _handle_health(self, id, delta):
        new_health = self.snakes[id]["health"] + delta
        self.snakes[id]["health"] = clamp(new_health, 0 , 100)
    
    def _is_outofbound(self, pos: tuple):
        return pos[0] >= self.width or pos[0] < 0 or pos[1] >= self.height or pos[1] < 0
    
# Utility Functions
def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def pos_to_tuple(pos: dict) -> tuple[int, int]:
    return (pos["x"], pos["y"])

def tuple_to_pos(xy: tuple[int, int]) -> dict:
    return {"x": xy[0], "y": xy[1]}
    