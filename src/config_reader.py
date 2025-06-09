import tomllib
from typing import Final

CELL_SIZE = 0
with open('src/config.toml', mode='rb') as file:
    config = tomllib.load(file)
    CELL_SIZE = config['cell_size']