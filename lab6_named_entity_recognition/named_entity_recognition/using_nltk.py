from typing import List

from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

from named_entity_recognition.utils import load_text, save_list


def main():
    text = load_text('hayek.txt')
    names = sorted_unique(find_named_entities(text))
    save_list('nltk.txt', names)


def sorted_unique(list: List):
    return sorted(set(list))


def find_named_entities(text: str):
    # https://stackoverflow.com/a/31838373/5114473
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    named_entities = [' '.join([token for token, pos in ne.leaves()])
                      for ne in chunked if type(ne) is Tree]
    return named_entities


if __name__ == '__main__':
    main()
