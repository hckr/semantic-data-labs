from typing import Iterable, List

import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

def load_text(file_path: str) -> str:
    with open(os.path.join(CURRENT_DIR, file_path)) as f:
        return f.read()


def save_text(file_path: str, text: str) -> None:
    with open(os.path.join(CURRENT_DIR, file_path), 'w') as f:
        return f.write(text)


def save_list(file_name: str, list: List) -> None:
    with open(os.path.join(CURRENT_DIR, f'output/{file_name}'), 'w') as f:
        for el in list:
            f.write(f'{el}\n')


def load_list(file_path: str) -> List[str]:
    with open(os.path.join(CURRENT_DIR, file_path)) as f:
        return [x.strip() for x in f.readlines()]

def join_with_newlines(x: Iterable[str]) -> str:
        return '\n'.join(x)
