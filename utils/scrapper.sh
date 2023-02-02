#!/bin/bash

# Activate virtual environment
VENV_PATH=/home/django/Desktop/programing/PokemonTCG-PriceScraper/venv
source $VENV_PATH/bin/activate

# Run Python script
python /home/django/Desktop/programing/PokemonTCG-PriceScraper/main.py

# Deactivate virtual environment
deactivate
