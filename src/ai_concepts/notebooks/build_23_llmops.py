"""Build notebooks/23_llmops.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_23_llmops.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 23 · LLMOps\n'
    '\n'
    '> Lifecycle practices for building, versioning, evaluating, deploying, and monitoring LLM apps.\n'
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
    "stages = ['build + version', 'evaluate', 'deploy', 'monitor']\n"
    'for i in range(len(stages) + 1):\n'
    "    print(stages[i % len(stages)], end=' -> ' if i < len(stages) else '\\n')\n"
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
    build("23_llmops", cells)
