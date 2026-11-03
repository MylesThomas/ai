"""Build 01_tokens.ipynb + .html (same folder). Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_01_tokens.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 01 · Tokens\n'
    '\n'
    '> The units of text a model reads, writes and is billed by. A token is usually a word or part of a word.\n'
))

cells.append(md(
    '## What it is\n'
    '\n'
    '- A tokenizer breaks text into pieces from a fixed vocabulary and maps each piece to an integer ID. '
    'The model only ever sees those IDs.\n'
    '- A token is roughly ¾ of an English word, about 4 characters. Code, other languages and emoji take more tokens.\n'
))

cells.append(md(
    '## Why it matters\n'
    '\n'
    '- **Cost:** you pay per input token and per output token.\n'
    '- **Limits:** context windows and `max_tokens` are measured in tokens, not characters or words.\n'
    '- **Behavior:** the model sees chunks, not letters, which explains why it struggles with spelling, '
    'letter counting and arithmetic.\n'
))

cells.append(code(
    'import os\n'
    'import tiktoken\n'
    '\n'
    "enc = tiktoken.get_encoding('o200k_base')  # OpenAI's GPT-4o tokenizer\n"
    '\n'
    'def show(text):\n'
    '    """Print each token of text between | bars, plus the count."""\n'
    '    ids = enc.encode(text)\n'
    "    pieces = [enc.decode([i]) for i in ids]\n"
    "    print(f'{len(ids):>3} tokens  |' + '|'.join(pieces) + '|')\n"
    '    return ids\n'
))

# --- 1. See the pieces -------------------------------------------------------

cells.append(md(
    '## 1 · See the pieces\n'
    '\n'
    'Common words are one token; rare words split into chunks. A leading space is part of the token.\n'
))

cells.append(code(
    "for s in ['hello', ' hello', 'Hello', 'HELLO',\n"
    "          'unbelievably', 'antidisestablishmentarianism',\n"
    "          'Tokenization splits unbelievably long words into pieces.']:\n"
    '    show(s)\n'
    '\n'
    "print()\n"
    "print('hello  ->', enc.encode('hello'))\n"
    "print(' hello ->', enc.encode(' hello'), ' (different id!)')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Models don\'t read words or letters. They read token IDs: integers from a fixed vocabulary (~200k entries for o200k).\n'
    '- Common words are one token; rare words are built from sub-word chunks (`un|bel|ievably`).\n'
    '- Leading spaces and capitalization are part of the token: `"hello"`, `" hello"`, `"HELLO"` are all different. The same word can tokenize differently depending on where it appears.\n'
))

# --- 2. Chars per token ------------------------------------------------------

cells.append(md(
    '## 2 · The ~4 chars/token rule, and where it breaks\n'
))

cells.append(code(
    'samples = {\n'
    "    'English': 'The quick brown fox jumps over the lazy dog near the riverbank.',\n"
    "    'Python':  'def add(a, b):\\n    return a + b  # simple helper\\n',\n"
    "    'JSON':    '{\"user_id\": 48213, \"tags\": [\"a\", \"b\"], \"active\": true}',\n"
    "    'URL':     'https://example.com/api/v2/users?id=48213&sort=desc',\n"
    "    'Spanish': 'El rápido zorro marrón salta sobre el perro perezoso.',\n"
    "    'Japanese': '素早い茶色の狐が怠け者の犬を飛び越える。',\n"
    "    'Emoji':   '🎉🔥🚀👍😂🙏',\n"
    "    'UUID':    '3f2b8c1e-9d4a-4e7b-a1c2-7f6e5d4c3b2a',\n"
    '}\n'
    '\n'
    "print(f\"{'type':<9}{'chars':>6}{'tokens':>8}{'chars/tok':>11}\")\n"
    'for name, text in samples.items():\n'
    '    n = len(enc.encode(text))\n'
    "    print(f'{name:<9}{len(text):>6}{n:>8}{len(text) / n:>11.2f}')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- ~4 chars/token is a rule of thumb for **English prose only**.\n'
    '- Code, JSON, and URLs are ~2.5-3 (symbols, odd fragments). Japanese, emoji, and random IDs like UUIDs are ~1 or less.\n'
    '- Same character count can mean much more cost and context-window usage. Count tokens, don\'t estimate from characters.\n'
))

# --- 3. Counting letters -----------------------------------------------------

cells.append(md(
    '## 3 · Why models are bad at counting letters\n'
    '\n'
    'The model sees token ids, not characters. "How many r\'s in strawberry?" asks about '
    'something that is not directly in its input.\n'
))

cells.append(code(
    "for s in ['strawberry', ' strawberry', 'yrrebwarts', '12345678', '1234 + 5678 = 6912']:\n"
    '    show(s)\n'
    '\n'
    "print()\n"
    "print('what the model gets for strawberry:', enc.encode('strawberry'))\n"
    "print(\"actual r count (Python sees chars):\", 'strawberry'.count('r'))\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- `strawberry` arrives as `[st, raw, berry]`: three IDs, no letters. Counting r\'s means recalling how each chunk is spelled, not looking.\n'
    '- Numbers split into irregular chunks (`123|4`, `691|2`), so digits don\'t line up by place value. Part of why arithmetic and spelling go wrong.\n'
    '- Fix: hand these tasks to code (a tool call) instead of asking the model to do them in its head.\n'
))

# --- 4. Cost -----------------------------------------------------------------

cells.append(md(
    '## 4 · Counting tokens for cost\n'
    '\n'
    'You pay per input token and per output token. Output is usually about 5× the price. '
    '`max_tokens` caps the output side.\n'
    '\n'
    'tiktoken is OpenAI\'s tokenizer, so for Claude it only gives an **estimate**. '
    'Anthropic\'s `count_tokens` endpoint gives exact counts (free, needs an API key).\n'
))

cells.append(code(
    '# $ per 1M tokens (input, output). Anthropic list prices, Oct 2026.\n'
    'PRICES = {\n'
    "    'claude-opus-5-5':   (4.00, 20.00),\n"
    "    'claude-sonnet-5-5': (2.00, 10.00),\n"
    "    'claude-haiku-5-5':  (0.10,  0.50),\n"
    '}\n'
    '\n'
    'def estimate_cost(prompt, expected_output_tokens, model):\n'
    '    """Rough $ estimate using tiktoken counts as a stand-in for Claude\'s tokenizer."""\n'
    '    n_in = len(enc.encode(prompt))\n'
    '    p_in, p_out = PRICES[model]\n'
    '    return n_in, (n_in * p_in + expected_output_tokens * p_out) / 1_000_000\n'
    '\n'
    "prompt = samples['English'] * 200   # ~13k chars\n"
    'for model in PRICES:\n'
    '    n_in, usd = estimate_cost(prompt, expected_output_tokens=1_000, model=model)\n'
    "    print(f'{model:<18} in={n_in:>6} tok  out=1000 tok  ~${usd:.5f}')\n"
))

cells.append(code(
    '# Exact Claude count. Skipped unless ANTHROPIC_API_KEY is set.\n'
    "if os.environ.get('ANTHROPIC_API_KEY'):\n"
    '    import anthropic\n'
    '    client = anthropic.Anthropic(max_retries=0)\n'
    "    msgs = [{'role': 'user', 'content': prompt}]\n"
    "    exact = client.messages.count_tokens(model='claude-opus-5-5', messages=msgs).input_tokens\n"
    '    approx = len(enc.encode(prompt))\n'
    "    print(f'Claude exact: {exact}  |  tiktoken estimate: {approx}  |  ratio {exact / approx:.2f}')\n"
    'else:\n'
    "    print('ANTHROPIC_API_KEY not set: skipping exact Claude count_tokens call')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Cost = input tokens x input price + output tokens x output price. Output is ~5x more per token.\n'
    '- `max_tokens` caps output length (and output cost). Hitting it cuts the response off mid-answer.\n'
    '- Each model family has its own tokenizer, so tiktoken is only a rough estimate for Claude. Exact: Anthropic\'s `count_tokens` endpoint, or `response.usage` after a call.\n'
    '- Model choice moves price the most: Haiku is ~40x cheaper than Opus for the same prompt.\n'
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
    build("01_tokens", cells)
