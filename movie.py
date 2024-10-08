from dataclasses import dataclass


@dataclass
class Movie:
    name: str
    filter: str
    introduce: str
    post: str
    heat: int
