"""Build 05_semantic_search.ipynb + .html (same folder). Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_05_semantic_search.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 05 · Semantic search\n'
    '\n'
    '> Retrieving results by meaning similarity rather than exact keyword matches.\n'
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
    '# Placeholder: swap bag-of-words for real embeddings later\n'
    "docs = ['how to reset my password', 'billing and invoices', 'change login credentials']\n"
    "query = 'forgot password'\n"
    'score = lambda d: len(set(d.split()) & set(query.split()))\n'
    'print(sorted(docs, key=score, reverse=True))\n'
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
    build("05_semantic_search", cells)
