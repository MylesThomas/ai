"""Build notebooks/14_agentic_workflows.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_14_agentic_workflows.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 14 · Agentic workflows\n'
    '\n'
    '> Multi-step pipelines where LLMs make decisions and chain actions together.\n'
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
    "steps = [str.strip, str.lower, lambda s: s.replace(' ', '_')]\n"
    "x = '  Agentic Workflow Demo '\n"
    'for step in steps:\n'
    '    x = step(x)\n'
    'print(x)\n'
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
    build("14_agentic_workflows", cells)
