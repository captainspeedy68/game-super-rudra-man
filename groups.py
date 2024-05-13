from typing import Iterable, Union
from pygame.sprite import AbstractGroup
from settings import *


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()