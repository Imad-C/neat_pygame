# NEAT Pygame

NEAT Pygame is a hobby project exploring the use of reinforcement learning to teach an AI to play a custom game made in Pygame.

## Demo

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

* You can play the main game by running:
```bash
python -m src.my_game.main_game  
```

* You can train the AI by running:
```bash
python -m src.neat_ai.neat_ai train
```
Training is a somewhat random process, but on average takes about 10 generations for it to learn how to _beat_ the game (about 45 mintues).

* Once the AI is trained, you can watch it play by running:
```bash
python -m src.neat_ai.neat_ai test 
```
You can watch a pre-trained example by passing `test_example` instead of `test`.

* A hard coded AI can also be seen by running:
```bash
python -m src.my_game.main_game -a
```

## Notes

The NEAT config can be found in src/neat_ai/config.txt. Here, how the AI operates can be changed, mainly the `pop_size` argument which detirmines how many nueral nets are trained in each generation. 

The number of generations can be changed by adjusting the line `pop.run(eval_genomes, 30)` found in src/neat_ai/neat_ai.py, changing _30_ to a different number.

Find more information on NEAT and how the NEAT package works by going to the [official documentation](https://neat-python.readthedocs.io/en/latest/)