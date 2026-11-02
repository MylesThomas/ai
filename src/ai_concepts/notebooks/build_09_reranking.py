"""Build notebooks/09_reranking.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_09_reranking.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 09 · Reranking\n'
    '\n'
    '> Re-scoring retrieved results with a stronger model to surface the best ones.\n'
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
    "candidates = ['doc about cats', 'doc about cat food', 'doc about cars']\n"
    "query = 'what do cats eat'\n"
    '# Stand-in for a cross-encoder score\n'
    "rerank_score = lambda d: sum(w in d for w in ['cat', 'food', 'eat'])\n"
    'print(sorted(candidates, key=rerank_score, reverse=True))\n'
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
    build("09_reranking", cells)
