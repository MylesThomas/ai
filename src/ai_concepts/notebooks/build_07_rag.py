"""Build notebooks/07_rag.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_07_rag.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 07 · RAG\n'
    '\n'
    '> Retrieving relevant documents and feeding them to the model to ground answers.\n'
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
    "kb = {'refund': 'Refunds are processed within 5 days.', 'shipping': 'Shipping takes 2-3 days.'}\n"
    "question = 'How long do refunds take?'\n"
    'context = [v for k, v in kb.items() if k in question.lower()]\n'
    "prompt = 'Answer using only this context:\\n' + '\\n'.join(context) + '\\n\\nQ: ' + question\n"
    'print(prompt)\n'
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
    build("07_rag", cells)
