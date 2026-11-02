"""Build notebooks/22_llm_observability.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_22_llm_observability.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 22 · LLM observability\n'
    '\n'
    '> Tracing, logging, and monitoring LLM calls for cost, latency, and quality.\n'
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
    'import time\n'
    'traces = []\n'
    'def traced(fn):\n'
    '    def wrapper(*a):\n'
    '        t = time.perf_counter()\n'
    '        out = fn(*a)\n'
    "        traces.append({'fn': fn.__name__, 'ms': round((time.perf_counter() - t) * 1000, 3)})\n"
    '        return out\n'
    '    return wrapper\n'
    '@traced\n'
    'def call_llm(p):\n'
    '    return p.upper()\n'
    "call_llm('hello')\n"
    'print(traces)\n'
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
    build("22_llm_observability", cells)
