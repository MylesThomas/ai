"""Build 03_embeddings.ipynb + .html (same folder). Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_03_embeddings.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 03 · Embeddings\n'
    '\n'
    '> Numeric vectors capturing text meaning, so similar content sits close together.\n'
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
    'import math\n'
    'def cosine(a, b):\n'
    '    dot = sum(x * y for x, y in zip(a, b))\n'
    '    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))\n'
    'cat, kitten, car = [0.9, 0.1, 0.0], [0.85, 0.2, 0.05], [0.1, 0.0, 0.95]\n'
    "print('cat~kitten', round(cosine(cat, kitten), 3), '| cat~car', round(cosine(cat, car), 3))\n"
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
    build("03_embeddings", cells)
