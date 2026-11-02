"""Build notebooks/15_langgraph.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_15_langgraph.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 15 · LangGraph\n'
    '\n'
    '> Framework for building stateful, graph-based agent workflows with cycles and branching.\n'
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
    '# TODO: uv add langgraph, then build a StateGraph\n'
    "graph = {'start': 'retrieve', 'retrieve': 'generate', 'generate': 'end'}\n"
    "node = 'start'\n"
    "while node != 'end':\n"
    '    node = graph[node]\n'
    "    print('->', node)\n"
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
    build("15_langgraph", cells)
