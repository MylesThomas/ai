"""Build notebooks/11_structured_outputs.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_11_structured_outputs.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 11 · Structured outputs\n'
    '\n'
    '> Forcing model responses into defined schemas like JSON for reliable parsing.\n'
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
    'import json\n'
    'raw = \'{"name": "Ada", "age": 36}\'\n'
    'data = json.loads(raw)\n'
    "assert set(data) == {'name', 'age'} and isinstance(data['age'], int)\n"
    'print(data)\n'
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
    build("11_structured_outputs", cells)
