from pathlib import Path
import tomllib


CELL_SIZE = 0
with open(Path('src', 'config', 'config.toml'), mode='rb') as file:
    config = tomllib.load(file)
    CELL_SIZE: int = config['cell_size']