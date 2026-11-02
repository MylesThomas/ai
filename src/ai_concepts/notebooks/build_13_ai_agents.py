"""Build notebooks/13_ai_agents.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_13_ai_agents.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 13 · AI agents\n'
    '\n'
    '> LLM systems that plan, use tools, and act autonomously toward goals.\n'
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
    'def policy(state):\n'
    "    return 'search' if 'facts' not in state else 'finish'\n"
    'state = {}\n'
    "while (action := policy(state)) != 'finish':\n"
    "    print('action:', action)\n"
    "    state['facts'] = ['...']\n"
    "print('done', state)\n"
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
    build("13_ai_agents", cells)
