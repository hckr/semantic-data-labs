import json
import os
from typing import List, Tuple
from urllib.parse import quote

import urllib3

from named_entity_recognition.utils import (join_with_newlines, load_list,
                                            save_text)

LIMIT = 0


def main():
    api_key = os.getenv('API_KEY')
    assert api_key, 'Please set API_KEY for Google Knowledge Graph as an env variable'

    names = load_list('output/nltk.txt')
    names_with_classes = []
    for i, name in enumerate(names):
        if LIMIT > 0 and i > LIMIT:
            break
        retries = 0
        while True:
            try:
                print(f"({i + 1} / {len(names)}) {name}{' '*100}", end='\r')
                names_with_classes.append(
                    (name, fetch_classes_from_google(api_key, name)))
                break
            except Exception as exc:
                retries += 1
                if retries > 2:
                    print()
                    raise exc
            finally:
                pass
                # time.sleep(1)
    print(f"Saving HTML...{' '*100}")
    html = generate_html(names_with_classes)
    save_text('output/tagged_with_google_graph.html', html)


def fetch_classes_from_google(api_key: str, name: str) -> str:
    URL = 'https://kgsearch.googleapis.com/v1/entities:search?query={0}&key=' + api_key
    http = urllib3.PoolManager()
    response = http.request('GET', URL.format(quote(name)))
    jsonld = json.loads(response.data)
    classes = set()
    if 'itemListElement' not in jsonld:
        raise RuntimeError('Incorrect response: ' +
                           json.dumps(jsonld, indent=2))
    for item in jsonld['itemListElement']:
        try:
            for t in item['result']['@type']:
                classes.add(t)
        except KeyError:
            pass
    return ', '.join(sorted(classes))


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
