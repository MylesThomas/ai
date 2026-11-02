"""Build notebooks/20_ragas.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_20_ragas.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 20 · Ragas\n'
    '\n'
    '> Open-source framework for evaluating RAG pipelines on faithfulness, relevance, and more.\n'
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
    '# TODO: uv add ragas\n'
    "context = 'Refunds take 5 days.'\n"
    "answer = 'Refunds take 5 days and are free.'\n"
    "claims = ['Refunds take 5 days', 'are free']\n"
    'faithfulness = sum(c.lower() in context.lower() for c in claims) / len(claims)\n'
    "print('toy faithfulness:', faithfulness)\n"
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
    build("20_ragas", cells)
