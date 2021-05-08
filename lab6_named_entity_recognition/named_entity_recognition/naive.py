import re
from typing import List

from named_entity_recognition.utils import load_text, save_list


def main():
    text = load_text('hayek.txt')
    names = sorted_unique(find_named_entities(text))
    save_list('naive.txt', names)


def sorted_unique(list: List):
    return sorted(set(list))


def find_named_entities(text: str):
    return re.findall(
        r'''(
                (?:[A-Z][\w-]{2,})
                (?:[ ]
                    (?:
                        (?:(?:of|on|von|for|from|a|an|and|to)[ ]){,2}
                        (?:[A-Z][\w-]+)
                    )
                )*
            )
            [.,; ]?
        ''',
        text,
        re.VERBOSE
    )


if __name__ == '__main__':
    main()
