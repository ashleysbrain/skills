# OpenAlex Working Script

A complete, tested Python script for OpenAlex search with abstract decoding
and clean output. Validated in session 2026-07-06 for a meditation/MEG/
criticality paper search.

## Search + decode + display

```python
import json, urllib.request, sys

def search_openalex(query, per_page=10):
    """Search OpenAlex and return decoded results."""
    url = f"https://api.openalex.org/works?search={query.replace(' ', '+')}&per-page={per_page}"
    req = urllib.request.Request(url, headers={"User-Agent": "DivinityScience/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())

def decode_abstract(inverted_index):
    """Reconstruct plain-text abstract from OpenAlex inverted index."""
    if not inverted_index:
        return '(no abstract)'
    max_pos = max(pos for positions in inverted_index.values() for pos in positions)
    words = [''] * (max_pos + 1)
    for word, positions in inverted_index.items():
        for pos in positions:
            if pos < len(words):
                words[pos] = word
    return ' '.join(words)

def display_results(data, abstract_len=400):
    """Print clean readable results."""
    print(f"Total results: {data.get('meta', {}).get('count', 'unknown')}")
    print('---')
    for w in data.get('results', []):
        title = w.get('title', '')
        year = w.get('publication_year', '')
        doi = w.get('doi', '')
        authors = ', '.join(
            a['author']['display_name']
            for a in w.get('authorships', [])[:3]
        )
        abstract = decode_abstract(w.get('abstract_inverted_index', {}))
        print(f'{year} | {title}')
        print(f'  Authors: {authors}')
        print(f'  DOI: {doi}')
        print(f'  Abstract: {abstract[:abstract_len]}')
        print()

# Usage
if __name__ == '__main__':
    query = sys.argv[1] if len(sys.argv) > 1 else 'meditation MEG neural efficiency'
    data = search_openalex(query)
    display_results(data)
```

## Fetch single paper by DOI

```python
def fetch_by_doi(doi):
    """Fetch a single paper by full DOI URL."""
    url = f"https://api.openalex.org/works/{doi}"
    req = urllib.request.Request(url, headers={"User-Agent": "DivinityScience/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    
    title = data.get('title', '')
    year = data.get('publication_year', '')
    doi_val = data.get('doi', '')
    abstract = decode_abstract(data.get('abstract_inverted_index', {}))
    authors = ', '.join(
        a['author']['display_name']
        for a in data.get('authorships', [])
    )
    venue = data.get('primary_location', {}).get('source', {}).get('display_name', '')
    
    print(f'TITLE: {title}')
    print(f'YEAR: {year}')
    print(f'VENUE: {venue}')
    print(f'AUTHORS: {authors}')
    print(f'DOI: {doi_val}')
    print()
    print('FULL ABSTRACT:')
    print(abstract)

# Usage
fetch_by_doi('https://doi.org/10.1093/nc/niaf047')
```

## Iterative narrowing pattern

When the first search is too broad, use `meta.count` as your signal and
add specificity:

```python
# Round 1: broad (603 results)
search_openalex('meditation MEG connectivity efficiency')

# Round 2: add method terms (70 results)  
search_openalex('meditation magnetoencephalography graph theory small-world topology')

# Round 3: add population / context (fewer, more targeted)
search_openalex('meditation MEG whole brain network small-world efficiency experienced meditators')
```

Each round, check `meta.count`. You're looking for the sweet spot where
the target paper surfaces in the top 10. If it doesn't, change the
keyword combination rather than paging deeper.
