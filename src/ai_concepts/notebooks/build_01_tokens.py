"""Build 01_tokens.ipynb + .html (same folder). Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_01_tokens.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 01 · Tokens\n'
    '\n'
    '> Chunks of text (words/subwords) that models read, generate, and bill by.\n'
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
    "text = 'Tokenization splits unbelievably long words into pieces.'\n"
    'words = text.split()\n'
    'chars = list(text)\n'
    "print('chars:', len(chars), '| words:', len(words))\n"
    "print('rule of thumb (~4 chars/token):', round(len(text) / 4))\n"
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
    build("01_tokens", cells)
