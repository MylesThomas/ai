"""Build 16_langchain.ipynb + .html (same folder). Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_16_langchain.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 16 · LangChain\n'
    '\n'
    '> Popular framework providing components for chaining LLM calls, tools, and retrieval.\n'
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
    '# TODO: uv add langchain, then compose prompt | model | parser\n'
    "prompt = lambda topic: 'Explain ' + topic + ' in one line.'\n"
    "model = lambda p: '[model output for: ' + p + ']'\n"
    "print(model(prompt('LangChain')))\n"
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
    build("16_langchain", cells)
