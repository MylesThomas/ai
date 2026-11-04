"""Build 02_context_windows.ipynb + .html (same folder). Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/notebooks/build_02_context_windows.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 02 · Context windows\n'
    '\n'
    '> Maximum tokens a model can consider at once, including prompt and output.\n'
))

cells.append(md(
    '## What it is\n'
    '\n'
    '- The context window is the model\'s working memory for one request: system prompt + tools + '
    'every message in the conversation + the output it is writing. All of it is measured in tokens.\n'
    '- The model is stateless. It remembers nothing between calls; a "conversation" is you resending '
    'the whole history every turn.\n'
    '- Current Claude models (Opus / Sonnet / Haiku 5.5): **1M-token** window, up to **128K** output tokens.\n'
))

cells.append(md(
    '## Why it matters\n'
    '\n'
    '- **Hard limit:** input + `max_tokens` must fit, or the request fails (or the output gets cut off).\n'
    '- **Cost:** every turn you pay again for the whole history, so long chats get expensive fast.\n'
    '- **Quality:** more context isn\'t free. Models attend less reliably to stuff buried in the middle '
    'of a huge prompt, and latency grows with input size.\n'
))

cells.append(code(
    'import os\n'
    'import tiktoken\n'
    '\n'
    "enc = tiktoken.get_encoding('o200k_base')  # stand-in tokenizer (see 01)\n"
    '\n'
    'def ntok(text):\n'
    '    return len(enc.encode(text))\n'
    '\n'
    '# Current Claude limits (Nov 2026): (context window, max output)\n'
    'LIMITS = {\n'
    "    'claude-opus-5-5':   (1_000_000, 128_000),\n"
    "    'claude-sonnet-5-5': (1_000_000, 128_000),\n"
    "    'claude-haiku-5-5':  (1_000_000, 128_000),\n"
    '}\n'
    '# $ per 1M tokens (input, output)\n'
    'PRICES = {\n'
    "    'claude-opus-5-5':   (4.00, 20.00),\n"
    "    'claude-sonnet-5-5': (2.00, 10.00),\n"
    "    'claude-haiku-5-5':  (0.10,  0.50),\n"
    '}\n'
))

# --- 1. The budget -----------------------------------------------------------

cells.append(md(
    '## 1 · The budget: input + output must fit\n'
    '\n'
    'Output shares the window with the input. A big prompt leaves less room to answer.\n'
))

cells.append(code(
    "WINDOW, MAX_OUT = LIMITS['claude-opus-5-5']\n"
    '\n'
    'def fits(prompt_tokens, max_output, window=WINDOW):\n'
    '    """True if prompt + reserved output fit; also returns tokens left over."""\n'
    '    left = window - prompt_tokens - max_output\n'
    '    return left >= 0, left\n'
    '\n'
    'for prompt, out in [(150_000, 32_000), (900_000, 64_000), (950_000, 64_000), (990_000, 16_000)]:\n'
    '    ok, left = fits(prompt, out)\n'
    "    print(f'prompt={prompt:>9,}  max_output={out:>7,}  fits={str(ok):<5}  left={left:>8,}')\n"
))

cells.append(code(
    '# How much text is 1M tokens? Use a real paragraph to scale.\n'
    "para = ('The quick brown fox jumps over the lazy dog near the riverbank. ' * 10).strip()\n"
    'tok_per_para = ntok(para)\n'
    'words_per_para = len(para.split())\n'
    'paras = WINDOW // tok_per_para\n'
    "print(f'{tok_per_para} tokens per {words_per_para}-word paragraph')\n"
    "print(f'1M tokens ~ {paras * words_per_para:,} words ~ {paras * words_per_para // 90_000} novels (90k words each)')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Window = everything in one request: system + tools + history + new message + output.\n'
    '- `max_tokens` reserves output space. Too small and the answer is cut off (`stop_reason == "max_tokens"`); '
    'input + `max_tokens` over the window and the request is rejected.\n'
    '- 1M tokens is ~750-850k English words: several novels or a mid-sized codebase. Code and JSON fill it faster (see 01).\n'
))

# --- 2. Conversations grow ---------------------------------------------------

cells.append(md(
    '## 2 · Conversations resend everything\n'
    '\n'
    'The API is stateless. Turn N sends turns 1..N-1 again, so input tokens per call grow every turn '
    'and **total** tokens billed grow roughly with the square of the turn count.\n'
))

cells.append(code(
    'SYSTEM = 2_000        # system prompt + tool definitions\n'
    'USER_MSG = 300        # tokens per user message\n'
    'REPLY = 700           # tokens per assistant reply\n'
    "p_in, p_out = PRICES['claude-opus-5-5']\n"
    '\n'
    'history = SYSTEM\n'
    'total_in = total_out = 0\n'
    "print(f\"{'turn':>4}{'input this call':>17}{'cum input':>12}{'cum $':>9}\")\n"
    'for turn in range(1, 101):\n'
    '    call_in = history + USER_MSG\n'
    '    total_in += call_in\n'
    '    total_out += REPLY\n'
    '    history = call_in + REPLY      # reply becomes part of the next call\n'
    '    if turn in (1, 2, 5, 10, 25, 50, 100):\n'
    '        usd = (total_in * p_in + total_out * p_out) / 1e6\n'
    "        print(f'{turn:>4}{call_in:>17,}{total_in:>12,}{usd:>9.2f}')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Each call\'s input = everything so far. By turn 100 one call is ~100k tokens, even though each message is tiny.\n'
    '- Cumulative input is quadratic: 10x the turns is roughly 100x the input tokens. The long tail of a chat is what costs money.\n'
    '- Agents are worse: tool results (file contents, search hits) pile into history quickly.\n'
    '- Prompt caching helps: an unchanged prefix is billed at ~10% on repeat calls. It cuts cost, not context usage.\n'
))

# --- 3. When it overflows ----------------------------------------------------

cells.append(md(
    '## 3 · When history won\'t fit: trim or summarize\n'
    '\n'
    'Two basic strategies. **Sliding window:** drop the oldest turns. **Summarize:** replace old turns with '
    'a short summary. Always keep the system prompt.\n'
))

cells.append(code(
    'def make_history(n_turns):\n'
    '    msgs = []\n'
    '    for i in range(1, n_turns + 1):\n'
    "        msgs.append({'role': 'user', 'content': f'Question {i}: ' + 'details ' * 60})\n"
    "        msgs.append({'role': 'assistant', 'content': f'Answer {i}: ' + 'explanation ' * 150})\n"
    '    return msgs\n'
    '\n'
    'def count(msgs):\n'
    "    return sum(ntok(m['content']) for m in msgs)\n"
    '\n'
    'def sliding_window(msgs, budget):\n'
    '    """Keep the most recent whole user/assistant pairs that fit in budget."""\n'
    '    kept = []\n'
    '    for i in range(len(msgs) - 2, -1, -2):\n'
    '        pair = msgs[i:i + 2]\n'
    '        if count(kept) + count(pair) > budget:\n'
    '            break\n'
    '        kept = pair + kept\n'
    '    return kept\n'
    '\n'
    'msgs = make_history(40)\n'
    'budget = 2_000\n'
    'trimmed = sliding_window(msgs, budget)\n'
    "print(f'full history: {len(msgs)} msgs, {count(msgs):,} tokens')\n"
    "print(f'sliding window ({budget:,} budget): {len(trimmed)} msgs, {count(trimmed):,} tokens')\n"
    "print('oldest kept:', trimmed[0]['content'][:12], '...')\n"
))

cells.append(code(
    '# Summarize: old turns -> one short message, recent turns kept verbatim.\n'
    'KEEP_RECENT = 6  # messages\n'
    'old, recent = msgs[:-KEEP_RECENT], msgs[-KEEP_RECENT:]\n'
    '# In real code an LLM call writes this summary. Here we fake one.\n'
    "summary = {'role': 'user', 'content': 'Summary of earlier conversation: ' + 'key fact ' * 80}\n"
    'compacted = [summary] + recent\n'
    "print(f'old turns: {len(old)} msgs, {count(old):,} tokens  ->  summary: {count([summary]):,} tokens')\n"
    "print(f'compacted history: {len(compacted)} msgs, {count(compacted):,} tokens')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Sliding window: simple, but anything older than the window is gone (names, decisions, the original task).\n'
    '- Summarize/compact: keeps the gist of old turns at a fraction of the tokens. Costs an extra LLM call and loses detail.\n'
    '- Trim whole user/assistant pairs (and tool_use/tool_result pairs together), or the API rejects the malformed history.\n'
    '- Claude\'s API can do this server-side: **compaction** (beta) summarizes once history passes a threshold; '
    '**context editing** (beta) clears old tool results.\n'
    '- Better still: don\'t put it in context at all. Retrieve only what\'s relevant (RAG, topic 07; agent memory, topic 18).\n'
))

# --- 4. Bigger isn't free ----------------------------------------------------

cells.append(md(
    '## 4 · A full window costs real money\n'
    '\n'
    'What one call costs if you actually fill the window, per model.\n'
))

cells.append(code(
    'for model, (window, max_out) in LIMITS.items():\n'
    '    p_in, p_out = PRICES[model]\n'
    '    prompt = window - 8_000\n'
    "    if model == 'claude-haiku-5-5' and prompt > 100_000:\n"
    '        p_in, p_out = 0.50, 2.50  # Haiku 5.5 long-prompt rate (>100k input)\n'
    '    usd = (prompt * p_in + 8_000 * p_out) / 1e6\n'
    "    print(f'{model:<18} {prompt:>9,} in + 8,000 out  ~${usd:.2f} per call')\n"
))

cells.append(code(
    '# Exact limits from the Models API. Skipped unless ANTHROPIC_API_KEY is set.\n'
    "if os.environ.get('ANTHROPIC_API_KEY'):\n"
    '    import anthropic\n'
    '    client = anthropic.Anthropic(max_retries=0)\n'
    '    for model in LIMITS:\n'
    '        m = client.models.retrieve(model)\n'
    "        print(f'{model:<18} context={m.max_input_tokens:>9,}  max_output={m.max_tokens:>7,}')\n"
    'else:\n'
    "    print('ANTHROPIC_API_KEY not set: skipping Models API lookup')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- One full-window Opus call is ~$4. Haiku jumps to its long-prompt rate above 100k input. Do that every turn of an agent loop and it adds up quickly.\n'
    '- Latency grows with input: the model has to process every token before it writes the first output token.\n'
    '- "Lost in the middle": recall is best for things at the start or end of a long prompt. Put instructions '
    'and the question at the end, after the big documents.\n'
    '- Don\'t hardcode limits in real code. `client.models.retrieve(id)` returns `max_input_tokens` (window) and `max_tokens` (output cap).\n'
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
    build("02_context_windows", cells)
