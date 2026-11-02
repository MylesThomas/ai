"""Build notebooks/18_agent_memory.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_18_agent_memory.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 18 · Agent memory\n'
    '\n'
    '> Persisting information across steps or sessions so agents retain context.\n'
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
    'from collections import deque\n'
    'short_term = deque(maxlen=3)\n'
    'long_term = {}\n'
    "for msg in ['hi', 'my name is Myles', 'I like python', 'what is my name?']:\n"
    '    short_term.append(msg)\n'
    "    if 'my name is' in msg:\n"
    "        long_term['name'] = msg.split()[-1]\n"
    'print(list(short_term), long_term)\n'
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
    build("18_agent_memory", cells)
