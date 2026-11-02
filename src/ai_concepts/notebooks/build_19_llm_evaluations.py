"""Build 19_llm_evaluations.ipynb + .html (same folder). Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_19_llm_evaluations.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 19 · LLM evaluations\n'
    '\n'
    '> Systematically testing model outputs for quality, accuracy, and regressions.\n'
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
    "cases = [('2+2', '4'), ('capital of France', 'Paris')]\n"
    "fake_model = {'2+2': '4', 'capital of France': 'Lyon'}\n"
    'score = sum(fake_model[q] == a for q, a in cases) / len(cases)\n'
    "print('accuracy:', score)\n"
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
    build("19_llm_evaluations", cells)
