"""Build notebooks/04_vector_databases.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_04_vector_databases.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 04 · Vector databases\n'
    '\n'
    '> Stores built to index embeddings and quickly find nearest-neighbor matches.\n'
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
    'import math\n'
    "store = {'doc_a': [1, 0], 'doc_b': [0.7, 0.7], 'doc_c': [0, 1]}\n"
    'def knn(q, k=2):\n'
    '    return sorted(store, key=lambda d: math.dist(q, store[d]))[:k]\n'
    'print(knn([0.9, 0.2]))\n'
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
    build("04_vector_databases", cells)
