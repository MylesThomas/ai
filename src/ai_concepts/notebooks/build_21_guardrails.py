"""Build notebooks/21_guardrails.ipynb + .html. Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_21_guardrails.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 21 · Guardrails\n'
    '\n'
    '> Input/output checks that block unsafe, off-topic, or malformed model behavior.\n'
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
    'import re\n'
    'def output_guard(text):\n'
    "    return re.sub(r'\\b\\d{3}-\\d{2}-\\d{4}\\b', '[REDACTED]', text)\n"
    "print(output_guard('SSN is 123-45-6789'))\n"
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
    build("21_guardrails", cells)
