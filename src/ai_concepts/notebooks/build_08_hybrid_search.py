"""Build 08_hybrid_search.ipynb + .html (same folder). Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_08_hybrid_search.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 08 · Hybrid search\n'
    '\n'
    '> Combining keyword (BM25) and semantic vector search for better retrieval.\n'
))

cells.append(md(
    '## What it is\n'
    '\n'
    '- \n'
))

cells.append(md(
    '## Why it matters\n'
    '\n'
    '- \n'
))

cells.append(md('## Code\n'
))

cells.append(code(
    'def rrf(*rankings, k=60):\n'
    '    scores = {}\n'
    '    for ranking in rankings:\n'
    '        for rank, doc in enumerate(ranking):\n'
    '            scores[doc] = scores.get(doc, 0) + 1 / (k + rank + 1)\n'
    '    return sorted(scores, key=scores.get, reverse=True)\n'
    "print(rrf(['a', 'b', 'c'], ['c', 'a', 'd']))\n"
))

cells.append(md(
    '## Gotchas\n'
    '\n'
    '- \n'
))

cells.append(md(
    '## Resources\n'
    '\n'
    '- \n'
))

if __name__ == "__main__":
    build("08_hybrid_search", cells)
