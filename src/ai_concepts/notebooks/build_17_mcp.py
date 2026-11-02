"""Build 17_mcp.ipynb + .html (same folder). Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_17_mcp.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 17 · MCP\n'
    '\n'
    '> Model Context Protocol, an open standard for connecting models to tools/data.\n'
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
    '# TODO: uv add mcp, then write a minimal server\n'
    "manifest = {'tools': [{'name': 'get_weather', 'input_schema': {'city': 'string'}}]}\n"
    'print(manifest)\n'
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
    build("17_mcp", cells)
