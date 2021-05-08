import time
import urllib
from typing import List, Tuple

from SPARQLWrapper import JSON, SPARQLWrapper

from named_entity_recognition.utils import (join_with_newlines, load_list,
                                            save_text)

LIMIT = 0


def main():
    names = load_list('output/nltk.txt')
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    names_with_classes = []
    for i, name in enumerate(names):
        if LIMIT > 0 and i > LIMIT:
            break
        retries = 0
        while True:
            try:
                print(f"({i + 1} / {len(names)}) {name}{' '*100}", end='\r')
                names_with_classes.append(
                    (name, fetch_classes_from_wikidata(sparql, name)))
                break
            except urllib.error.HTTPError as exc:
                retries += 1
                if retries > 2:
                    print()
                    raise exc
            finally:
                time.sleep(2)
    print(f"Saving HTML...{' '*100}")
    html = generate_html(names_with_classes)
    save_text('output/tagged_with_wikidata.html', html)


def fetch_classes_from_wikidata(sparql: SPARQLWrapper, name: str) -> str:
    separator = ', '
    sparql.setQuery(f'''
    SELECT (GROUP_CONCAT(DISTINCT ?instanceOfName; SEPARATOR="{separator}") AS ?instanceOfNames) {{
    ?item rdfs:label "{name}"@en .
    ?item wdt:P31 ?instanceOf .
    ?instanceOf rdfs:label ?instanceOfName FILTER(LANG(?instanceOfName) = "en") .
    }}
    ''')
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()['results']['bindings'][0]['instanceOfNames']['value']


def generate_html(names_with_classes: List[Tuple[str, str]]) -> str:
    css = '''
table { border-collapse: collapse; max-width: 1000px; margin: 0 auto; }
tr { border-bottom: 1px solid #333 }
td { min-width: 200px; }
'''

    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
<style>{css}</style>
</head>
<body>
<table>
<tr><th>Name</th><th>Classes</th></tr>
{ join_with_newlines(f'<tr><td>{name}</td><td>{classes}</td></tr>' for (name, classes) in names_with_classes) }
</table>
</body>
</html>
'''.lstrip()


if __name__ == '__main__':
    main()
