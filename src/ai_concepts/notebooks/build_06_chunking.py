"""Build 06_chunking.ipynb + .html (same folder). Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_06_chunking.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 06 · Chunking\n'
    '\n'
    '> Splitting documents into smaller pieces sized for embedding and retrieval.\n'
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
    'def chunk(text, size=40, overlap=10):\n'
    '    step = size - overlap\n'
    '    return [text[i:i + size] for i in range(0, len(text), step)]\n'
    "for c in chunk('Chunking strategy matters: fixed-size, sentence, recursive, semantic, and more.'):\n"
    '    print(repr(c))\n'
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
    build("06_chunking", cells)
