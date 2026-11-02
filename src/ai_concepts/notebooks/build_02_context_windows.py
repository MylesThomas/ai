"""Build notebooks/02_context_windows.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_02_context_windows.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 02 · Context windows\n'
    '\n'
    '> Maximum tokens a model can consider at once, including prompt and output.\n'
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
    'WINDOW = 200_000\n'
    'def fits(prompt_tokens, max_output):\n'
    '    return prompt_tokens + max_output <= WINDOW\n'
    'print(fits(150_000, 32_000), fits(190_000, 32_000))\n'
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
    build("02_context_windows", cells)
