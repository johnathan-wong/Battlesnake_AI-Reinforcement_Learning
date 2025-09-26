# Battlesnake AI: Reinforcement Learning Agent 
This project implements a Battlesnake AI using Reinforcement Learning. The agenet is trained using the **Proximal Policy Potimization (PPO)** algorithm from the Stable-Baselines3 library, within a custom Gymnasium environment. The goal in this project is to create a robust and intelligent snake that can compete in Battlesnake game.

## Features
- Reinforcement Learning: Utilizes the PPO algorithm for training a AI policy
- Custom Game Engine: A custom game engine to simulate the battlesnake game
- Custom Gymnasium Environment: A custom environment that provides the necessary observation, reward, and action spaces for RL training.
- Multiple Opponent: Contain multiple opponent to train the RL agent.
    - Improved Random Snake: Serves as a weak but unpredictable nature. It incorporates minor safety check like avoid self, wall and immediate opponent.
    - Custom Greedy Snake: Serves as a strong, predictable and exploitable adversary. It targets the closest foods, but also have caution to avoid other opponent's movement
- Multi-Input Observation: The agent's state is represents by a muti-input observation space, combining a grid-based view of the board and a vector of snake statistics.

## Prerequisites
Before running the project, you will need to have the following:
- Python 3.9+
- Git
- Battlesnake CLI

All reuired Python libraries can be installed via the `requirments.txt` file.

## Getting Started
### 1. Set Up the Python Environment (Optional)
```
# Create A Virtual Envirnment
python -m venv venv

# Activate The Virtual Envirnment
# MacOS/Linux:
source venv/bin/activate
# Windows (Command Prompt):
venv\Scripts\activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

```
### 2. Install dependencies
```
pip install -r reuirements.txt
```

### 3. Training the AI
To train a new PPO model, run the `training_ground.py` script. In the code you can configure the training setting. The default training setting is configured to run for 50,000 games on a 7x7 board.
```
python training_ground.py
```

### 4. Running the Battlesnake Server
Once you have a trained model(named `snake_rl_model` by default), you can tun it against other snakesusing the included Battlesnake server.
```
python main.py [<SnakeClassName>] [<port>]
```
| Argument | Description | Default |
| :--- | :--- | :--- |
| `[<SnakeClassName>]` | The name of the snake class to run (e.g., `NNSnake`, `AlgorithmSnake`). | `AlgorithmSnake` (if omitted) |
| `[<port>]` | The port number on which the server will listen. | `3000` |

Example 1:
```
# Hosted on http://localhost:3000
python main.py NNSnake
```
Example 2:
```
# Hosted on http://localhost:8000
python main.py NNSnake 8000
```

### 5. Run Local Game
Install the Battlesnake CLI

Example (required **3 command prompts**):
```
# Hosting NNSnake on port 8000
python main.py NNSnake 8000
```
```
# Hosting Greedy on port 3000
python main.py AlgorithmSnake 3000
```
```
# Play the game
battlesnake play -W 7 -H 7 --name RL-Agent --url http://localhost:8000 --name snake1 --url http://localhost:3000 --browser
```

## Project Structure
```
.
├── Gym/
│   ├── environment.py          # The custom Battlesnake Gymnasium environment
|   └── engine.py               # The custom Battlesnake Game Engine 
├── SnakeClasses/       
│   ├── base_snake.py           # Base class for all snakes (Also the random snake)
│   ├── AISnake/        
│   │   └── snake_nn.py         # The NNSnake class that uses the trained model
│   └── AlgorithmSnake/
│       └── algorithm_snake.py  # A greedy-based snake for competition
├── logs/                       # TensorBoard logs for training visualization
├── main.py                     # The Battlesnake server entry point
├── requirements.txt            # All Python dependencies
├── training_ground.py          # The training script for the RL model
└── snake_rl_model.zip          # The NN for the RL agent (50,000 games, 7x7 board)
```

## Next Steps
### Improvement
You can continue improve the RL agent by

- Adding more opponents
- Adding randomization to what kind of opponent to face
- Modify the observation space
### Compete in Battlesnake
Host your trained battlesnake onto a live web server and compete it on [play.battlesnake.com](play.battlesnake.com )

