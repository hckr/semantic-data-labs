# Named Entity Recognition

Text in [hayek.txt](hayek.txt) is taken from https://en.wikipedia.org/wiki/Friedrich_Hayek

## Initial setup

Probably the easiest would be to install requirements using [Poetry](https://python-poetry.org/docs/).

```bash
poetry install
```

## Native

Naive version implemented in [named_entity_recognition/naive.py](named_entity_recognition/naive.py) uses a regex to extract proper names.

```bash
poetry run python named_entity_recognition/naive.py
```

Results are saved to [named_entity_recognition/output/naive.txt](named_entity_recognition/output/naive.txt).

## NLTK

Version implemented in [named_entity_recognition/using_nltk.py](named_entity_recognition/using_nltk.py) uses NLTK's word tokenizer, part of speech tagger, and finally named entities chunker.

```bash
poetry run python named_entity_recognition/using_nltk.py
```

Results are saved to [named_entity_recognition/output/naive.txt](named_entity_recognition/output/nltk.txt).

### Initial setup

In order for all used NLTK's features to work, certain data must be downloaded before first run:

```bash
$ poetry run python
...
>>> import nltk
>>> nltk.download('punkt')
...
>>> nltk.download('averaged_perceptron_tagger')
...
>>> nltk.download('maxent_ne_chunker')
...
>>> nltk.download('words')
...
```

## Tag with Wikidata (SPARQL)

Named entites found with NLTK are annotated with what they are instances of accorcing to Wikidata, see implementation in [named_entity_recognition/tag_with_wikidata_sparql.py](named_entity_recognition/tag_with_wikidata_sparql.py).

```bash
poetry run python named_entity_recognition/tag_with_wikidata_sparql.py
```

Results are saved to HTML table in [named_entity_recognition/output/tagged_with_wikidata.html](named_entity_recognition/output/tagged_with_wikidata.html).

## Tag with Google Knowledge Graph Search API

Named entites found with NLTK are annotated with what type they are accorcing to Knowledge Graph, see implementation in [named_entity_recognition/tag_with_google_knowledge_graph.py](named_entity_recognition/tag_with_google_knowledge_graph.py). You need to get API key from [here](https://console.cloud.google.com/flows/enableapi?apiid=kgsearch.googleapis.com&credential=client_key).

```bash
API_KEY={put your API key here} poetry run python named_entity_recognition/tag_with_google_knowledge_graph.py
```

Results are saved to HTML table in [named_entity_recognition/output/tagged_with_google_graph.html](named_entity_recognition/output/tagged_with_google_graph.html).
