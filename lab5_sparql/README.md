# SPARQL

## Useful links

### Tutorials

* [Video: Querying Wikidata with SPARQL for Absolute Beginners](https://www.youtube.com/watch?v=kJph4q0Im98)
* [Slides: An Introduction to SPARQL](https://www.slideshare.net/olafhartig/an-introduction-to-sparql)
* [SPARQL tutorial on Wikidata](https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial)

### [SPARQL endpoints](https://www.w3.org/wiki/SparqlEndpoints)

* [DBpedia](https://dbpedia.org/sparql)
* [Wikidata](https://query.wikidata.org/)
* [MusicBrainz](http://dbtune.org/musicbrainz/snorql/)
* [European Bioinformatics Institute](https://www.ebi.ac.uk/rdf/services/sparql)

## Queries

### Countries

#### Names and populations (ordered) of all countries that have more than 10.000.000 inhabitants

```sparql
SELECT ?country ?countryLabel ?population {
  $country wdt:P31 wd:Q3624078 . # country is a sovereign state
  ?country wdt:P1082 ?population .
  FILTER (?population > 10000000)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
} ORDER BY DESC(?population)
```

([see in Wikidata Query Service](https://w.wiki/3Ciu))

#### Names of all countries that have at least one city with more than 1.000.000 inhabitants

```sparql
SELECT DISTINCT ?country ?countryLabel {
  ?city wdt:P31 wd:Q515 .
  ?city wdt:P1082 ?cityPopulation .
  FILTER (?cityPopulation > 1000000)
  ?city wdt:P17 ?country .
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
ORDER BY ?countryLabel
```

([see in Wikidata Query Service](https://w.wiki/3Cif))

Also with all cities which matched criteria, ordered by number of these cities:

```sparql
SELECT ?country ?countryName (GROUP_CONCAT(?cityName; SEPARATOR=", ") AS ?cityNames) {
  ?city wdt:P31 wd:Q515 .
  ?city wdt:P1082 ?cityPopulation .
  FILTER (?cityPopulation > 1000000)
  ?city wdt:P17 ?country .
  
  ?country rdfs:label ?countryName FILTER (LANG(?countryName) = "en") .
  ?city rdfs:label ?cityName FILTER (LANG(?cityName) = "en") .
}
GROUP BY ?country ?countryName
ORDER BY DESC(COUNT(?city))
```

([see in Wikidata Query Service](https://w.wiki/3ChG))

#### Names of all countries that have no city with more than 1.000.000 inhabitants

```sparql
SELECT ?country ?countryLabel {
  $country wdt:P31 wd:Q3624078 . # country is a sovereign state
  
  MINUS {
    SELECT DISTINCT (?country_ AS $country) {
      ?city wdt:P31 wd:Q515 . # a city
      ?city wdt:P1082 ?cityPopulation .
      FILTER (?cityPopulation > 1000000)
      ?city wdt:P17 ?country_ . # a sovereign state of the city
    }
  }
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
ORDER BY ?countryLabel
```

([see in Wikidata Query Service](https://w.wiki/3Cix))

#### Names of all european countries that have no membership in the European Union

```sparql
SELECT ?country ?countryLabel {
  $country wdt:P31 wd:Q3624078 . # country is a sovereign state
  $country wdt:P30 wd:Q46 . # country is in Europe
  MINUS {
    $country wdt:P463 wd:Q458 . # country is not in EU
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
ORDER BY ?countryLabel
```

([see in Wikidata Query Service](https://w.wiki/3Cit))

Also with countries which used to be in the EU, but are no longer:

```sparql
SELECT ?country ?countryLabel {
  $country wdt:P31 wd:Q3624078 . # country is a sovereign state
  $country wdt:P30 wd:Q46 . # country is in Europe
  MINUS { # subtract countries
    ?memberOfStatement a wikibase:BestRank; ps:P463 wd:Q458. # which are in EU
    FILTER NOT EXISTS { ?memberOfStatement pq:P582 ?endTime. } # but not the ones which used to be
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
ORDER BY ?countryLabel
```

([see in Wikidata Query Service](https://w.wiki/3CkE))

#### Abbreviations of all organizations whose headquarter is located in the capital of a member country

```sparql
SELECT ?organization ?organizationLabel ?organizationShortName ?countryLabel ?capitalLabel {
  ?country wdt:P31 wd:Q3624078 . # country is a sovereign state
  ?country wdt:P463 ?organization . # organization country is a member of
  ?capital wdt:P1376 ?country .
  ?organization wdt:P159 ?capital . # headquarters located in the capital
  OPTIONAL {
    ?organization wdt:P1813 ?organizationShortName FILTER (LANG(?organizationShortName) = "en") .
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
ORDER BY ?organizationLabel
```

([see in Wikidata Query Service](https://w.wiki/3CkT))

### Movies

#### Facts true for all given movies

```sparql
SELECT ?predicate ?predName ?object ?objName ?objDesc {
  wd:Q185888 ?predicate ?object . # The Social Network (2010)
  wd:Q212792 ?predicate ?object . # Bolt (2008)
  wd:Q83495 ?predicate ?object . # The Matrix (1999)
  
  ?predicateobj wikibase:directClaim ?predicate . # mapping between wd:* and wdt:*
  ?predicateobj rdfs:label ?predName FILTER(LANG(?predName) = "en") .
  ?object rdfs:label ?objName FILTER(LANG(?objName) = "en") .
  ?object schema:description ?objDesc FILTER(LANG(?objDesc) = "en") .
}
```

([see in Wikidata Query Service](https://w.wiki/3EDU))

#### Facts different for given movies

(properties of each which aren't shared by the other two; this might be heavily over-engineered)

```sparql
SELECT DISTINCT
  ?predicate ?predDesc
  (GROUP_CONCAT(DISTINCT ?TheSocialNetworkValueName; SEPARATOR=", ") AS ?TheSocialNetworkValueNames)
  (GROUP_CONCAT(DISTINCT ?BoltValueName; SEPARATOR=", ") AS ?BoltValueNames)
  (GROUP_CONCAT(DISTINCT ?TheMatrixValueName; SEPARATOR=", ") AS ?TheMatrixValueNames)
{
  wd:Q185888 ?predicate ?TheSocialNetworkValue
    FILTER NOT EXISTS { wd:Q185888 ?predicate ?BoltValue }
    FILTER NOT EXISTS { wd:Q185888 ?predicate ?TheMatrixValue } .
  
  wd:Q212792 ?predicate ?BoltValue
    FILTER NOT EXISTS { wd:Q212792 ?predicate ?TheSocialNetworkValue }
    FILTER NOT EXISTS { wd:Q212792 ?predicate ?TheMatrixValue } .
  
  wd:Q83495 ?predicate ?TheMatrixValue
    FILTER NOT EXISTS { wd:Q83495 ?predicate ?TheSocialNetworkValue }
    FILTER NOT EXISTS { wd:Q83495 ?predicate ?BoltValue } .
  
  ?predicateobj wikibase:directClaim ?predicate . # mapping between wd:* and wdt:*
  ?predicateobj rdfs:label ?predDesc FILTER(LANG(?predDesc) = "en") .
  
  ?TheSocialNetworkValue rdfs:label ?TheSocialNetworkValueName FILTER(LANG(?TheSocialNetworkValueName) = "en") .
  ?BoltValue rdfs:label ?BoltValueName FILTER(LANG(?BoltValueName) = "en") .
  ?TheMatrixValue rdfs:label ?TheMatrixValueName FILTER(LANG(?TheMatrixValueName) = "en") .
}
GROUP BY ?predicate ?predDesc
LIMIT 5
```

([see in Wikidata Query Service](https://w.wiki/3EDh))

### Programming languages

#### Programming languages designed by Brendan Eich

```sparql
SELECT ?programmingLanguage ?programmingLanguageLabel {
  ?programmingLanguage wdt:P31 wd:Q9143 .
  ?programmingLanguage wdt:P287 wd:Q92648 . # designed by Brendan Eich
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
```

([see in Wikidata Query Service](https://w.wiki/3Ckd))

#### JavaScript engines

```sparql
SELECT ?engine ?engineLabel {
  ?engine wdt:P31 wd:Q591919 . # is a JavaScript engine
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
```

([see in Wikidata Query Service](https://w.wiki/3Ckf))

#### Programming languages influenced by JavaScript

```sparql
SELECT ?lang ?langLabel {
  ?lang wdt:P31 wd:Q9143 . # a programming language
  ?lang wdt:P737 wd:Q2005 . # influenced by JavaScript
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
```

([see in Wikidata Query Service](https://w.wiki/3Ckh))

#### File extensions shared by multiple programming languages

```sparql
SELECT ?fileExtension (GROUP_CONCAT(DISTINCT ?langName; SEPARATOR=", ") AS ?langs) {
  ?lang wdt:P31 wd:Q9143 . # a programming language
  ?lang wdt:P1195 ?fileExtension .
  ?lang rdfs:label ?langName FILTER (LANG(?langName) = "en") .
}
GROUP BY ?fileExtension
HAVING (COUNT(?langName) > 1)
```

([see in Wikidata Query Service](https://w.wiki/3Ckn))

#### Languages with support for functional paradigm without imperative concepts

```sparql
SELECT ?lang ?langLabel {
  ?lang wdt:P31 wd:Q9143 . # a programming language
  ?lang wdt:P3966 wd:Q193076 .
  MINUS { ?lang wdt:P3966 wd:Q275596 . } # imperative programming
  MINUS { ?lang wdt:P3966 wd:Q1418502 . } # procedural programming
  MINUS { ?lang wdt:P3966 wd:Q4306983 . } # multi-paradigm programming
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
```

([see in Wikidata Query Service](https://w.wiki/3Ckp))

#### Software written in PHP

```sparql
SELECT ?software ?softwareLabel {
  ?software wdt:P277 wd:Q59 . # written in PHP
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
```

([see in Wikidata Query Service](https://w.wiki/3Ckz))
