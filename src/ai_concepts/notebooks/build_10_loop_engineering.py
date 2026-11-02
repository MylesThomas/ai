"""Build notebooks/10_loop_engineering.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_10_loop_engineering.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 10 · Loop engineering\n'
    '\n'
    '> Designing the iterative think-act-observe cycle that drives agent behavior.\n'
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
    'def fake_llm(attempt):\n'
    "    return 'draft' if attempt < 2 else 'final answer'\n"
    'for attempt in range(5):\n'
    '    out = fake_llm(attempt)\n'
    '    print(attempt, out)\n'
    "    if out == 'final answer':\n"
    '        break\n'
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
    build("10_loop_engineering", cells)
