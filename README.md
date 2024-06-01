# NEAT Pygame

NEAT Pygame is a hobby project exploring the use of reinforcement learning to teach an AI to play a custom game made in Pygame.

## Visual

Need to put a gif of the generational development here...

## Installation 

First clone the repo. 

```bash
git clone "https://github.com/Imad-C/neat_pygame.git"
```

Then install the required packages within your env.

```bash
pip install -r requirements.txt
```

## Usage

Ensuring you're within the root directory:

You can play the main game by running:
```bash
python -m src.my_game.main_game  
```

You can train the AI by running:
```bash
python -m src.my_game.main_game  
```

Once the AI is trained, you can watch it play by running:
```bash
python -m src.neat_ai.neat_ai argv[0]  
```