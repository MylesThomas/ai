"""Build 12_function_calling.ipynb + .html (same folder). Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_12_function_calling.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 12 · Function calling\n'
    '\n'
    '> Model outputs structured requests to invoke external tools or APIs.\n'
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
    "TOOLS = {'add': lambda a, b: a + b}\n"
    "model_output = {'tool': 'add', 'args': {'a': 2, 'b': 3}}\n"
    "result = TOOLS[model_output['tool']](**model_output['args'])\n"
    "print('tool result ->', result)\n"
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
    build("12_function_calling", cells)
