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
    '- An embedding model turns a piece of text into a fixed-length list of floats (here 384). '
    'Texts with similar meaning get vectors that point in similar directions.\n'
    '- "Close" is measured with **cosine similarity**: 1 = same direction, 0 = unrelated, negative = opposite.\n'
    '- It is a separate, much smaller model than a chat LLM. It reads text and outputs a vector; it doesn\'t generate anything.\n'
))

cells.append(md(
    '## Why it matters\n'
    '\n'
    '- It is how you search by **meaning** instead of exact words: the core of semantic search, RAG, '
    'recommendation, clustering and dedup (topics 04-09).\n'
    '- Cheap and fast: embed your documents once, store the vectors, compare with simple math at query time.\n'
))

cells.append(code(
    'import numpy as np\n'
    'from fastembed import TextEmbedding\n'
    '\n'
    "# Small open model (~130 MB download on first run), runs locally on CPU.\n"
    "model = TextEmbedding('BAAI/bge-small-en-v1.5')\n"
    '\n'
    'def embed(texts):\n'
    '    """List of strings -> (n, 384) array of unit-length vectors."""\n'
    '    return np.array(list(model.embed(texts)))\n'
    '\n'
    'def cosine(a, b):\n'
    '    """Cosine similarity, written out: dot product / product of lengths."""\n'
    '    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))\n'
))

# --- 1. What a vector looks like ---------------------------------------------

cells.append(md(
    '## 1 · What an embedding looks like\n'
))

cells.append(code(
    "v = embed(['The cat sat on the mat.'])[0]\n"
    "print('shape:', v.shape, ' dtype:', v.dtype)\n"
    "print('first 8 values:', np.round(v[:8], 3))\n"
    "print('length (L2 norm):', round(float(np.linalg.norm(v)), 4))\n"
    '\n'
    "short, long = embed(['Hi.', 'A much longer sentence about the history of maritime trade routes in the Mediterranean.'])\n"
    "print('short text shape:', short.shape, ' long text shape:', long.shape)\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Every input, one word or a whole paragraph, becomes the same size vector (384 floats for this model; '
    'bigger models use 768-3072).\n'
    '- Individual numbers mean nothing on their own. Only the direction of the whole vector matters.\n'
    '- This model returns unit-length vectors (norm = 1), so cosine similarity is just the dot product.\n'
))

# --- 2. Similarity -----------------------------------------------------------

cells.append(md(
    '## 2 · Similar meaning, similar vectors\n'
))

cells.append(code(
    'sents = [\n'
    "    'How do I reset my password?',\n"
    "    'I forgot my login credentials.',\n"
    "    'Steps to change your account password',\n"
    "    'The weather is sunny in Lisbon today.',\n"
    "    'Best pasta recipe with garlic and olive oil',\n"
    ']\n'
    'E = embed(sents)\n'
    'S = E @ E.T   # all pairwise cosine similarities (vectors are unit length)\n'
    '\n'
    "labels = ['reset pw', 'forgot login', 'change pw', 'weather', 'pasta']\n"
    "print(' ' * 13 + ''.join(f'{l:>13}' for l in labels))\n"
    'for l, row in zip(labels, S):\n'
    "    print(f'{l:<13}' + ''.join(f'{x:>13.2f}' for x in row))\n"
    '\n'
    "print('\\nhand-written cosine == dot product:', round(cosine(E[0], E[1]), 4), round(float(E[0] @ E[1]), 4))\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- The three password/login sentences score high with each other even though "forgot my login credentials" '
    'shares no words with "reset my password".\n'
    '- Unrelated sentences still score ~0.3-0.5, not 0. Each model has its own baseline, so scores are only '
    'meaningful **relative to each other**. Don\'t hardcode a threshold like 0.8 without testing on your data.\n'
))

# --- 3. Meaning vs words -----------------------------------------------------

cells.append(md(
    '## 3 · Meaning beats word overlap, mostly\n'
    '\n'
    'Compare a keyword measure (share of words in common) with embedding similarity.\n'
))

cells.append(code(
    'def word_overlap(a, b):\n'
    '    """Jaccard: shared words / total distinct words."""\n'
    "    wa, wb = set(a.lower().strip('.').split()), set(b.lower().strip('.').split())\n"
    '    return len(wa & wb) / len(wa | wb)\n'
    '\n'
    'pairs = [\n'
    "    ('The central bank raised interest rates.', 'The Fed hiked borrowing costs.'),\n"
    "    ('The central bank raised interest rates.', 'We sat on the river bank.'),\n"
    "    ('The movie was fantastic.', 'The film was great.'),\n"
    "    ('I love this product.', 'I do not love this product.'),\n"
    "    ('The dog bit the man.', 'The man bit the dog.'),\n"
    ']\n'
    "print(f\"{'overlap':>8}{'embed':>7}   pair\")\n"
    'for a, b in pairs:\n'
    '    ea, eb = embed([a, b])\n'
    "    print(f'{word_overlap(a, b):>8.2f}{cosine(ea, eb):>7.2f}   {a}  |  {b}')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Synonyms and paraphrases ("hiked borrowing costs", "film was great") score high with almost no shared words. Keyword search would miss them.\n'
    '- Same word, different sense ("central bank" vs "river bank") scores lower. The model uses context.\n'
    '- **Weak spots:** "love" vs "do not love" (opposite meaning) scores 0.70, higher than '
    'the two different kinds of "bank" (0.61). "Dog bit man" vs "man bit dog" scores 0.99. Embeddings capture what the text is *about*, '
    'not exactly what it *claims*.\n'
    '- Rare exact strings (error codes, SKUs, names) are also weak. That\'s why hybrid search (topic 08) adds keyword matching back in.\n'
))

# --- 4. Tiny search ----------------------------------------------------------

cells.append(md(
    '## 4 · A tiny semantic search\n'
    '\n'
    'Embed documents once, embed the query, rank by similarity. This is the whole idea behind topics 04-07.\n'
))

cells.append(code(
    'docs = [\n'
    "    'To reset your password, click \"Forgot password\" on the sign-in page.',\n"
    "    'Refunds are issued to the original payment method within 5-7 business days.',\n"
    "    'Our office is closed on public holidays.',\n"
    "    'You can export your data as CSV from the Settings > Data tab.',\n"
    "    'Two-factor authentication can be enabled under Security settings.',\n"
    "    'Shipping to Canada takes 3-5 business days.',\n"
    ']\n'
    '# bge models expect queries and documents to be embedded slightly differently.\n'
    'D = np.array(list(model.passage_embed(docs)))      # embed every doc once -> (6, 384) matrix, one row per doc\n'
    '\n'
    'def search(query, k=2):                            # return the k docs closest in meaning to query\n'
    '    q = np.array(list(model.query_embed(query)))[0]  # embed the query (query mode) -> one 384-dim vector\n'
    '    scores = D @ q                                 # dot product of q with every doc row = cosine similarity per doc\n'
    '    for i in np.argsort(-scores)[:k]:              # doc indexes sorted highest score first, keep the top k\n'
    "        print(f'  {scores[i]:.2f}  {docs[i]}')       # show the score and the matching doc\n"
    '\n'
    "for q in ['I can\\'t log in', 'how long until I get my money back', 'download my information', 'delivery time to Toronto']:\n"
    "    print(q)\n"
    '    search(q)\n'
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Every query finds the right doc without sharing keywords ("money back" -> refunds, "Toronto" -> Canada).\n'
    '- Documents are embedded **once** at index time; each query costs one small embedding call plus a matrix multiply.\n'
    '- Some models (bge, e5, Voyage) want a query vs document flag or prefix. Using the wrong one quietly lowers quality.\n'
    '- Brute force (`D @ q`) is fine for thousands of docs. For millions you need an index, which is what vector databases do (topic 04).\n'
))

# --- 5. EBITDA across five companies -----------------------------------------

cells.append(md(
    '## 5 · Looking up "EBITDA" across five companies\n'
    '\n'
    'Slide records shaped like the real deck data (one JSONL line per slide). The made-up fields '
    '`project` and `deck_stage` stand in for whatever the real data carries. Only `search_text` is the slide\'s words; '
    'everything else is **metadata**.\n'
    '\n'
    'Every company reports EBITDA, but the slides say it three ways: the acronym, spelled out, or '
    '"operating profit before D&A". Like real slides, the body text usually doesn\'t repeat the company name.\n'
))

cells.append(md(
    '### 5a · Searching for the metric\n'
))

cells.append(code(
    'slides = [\n'
    "    {'slide_id': 'nw-ic-07', 'deck_id': 'nw-ic', 'project': 'Northwind', 'deck_stage': 'Final IC', 'title': 'Financial Summary', 'slide_type': 'financials',\n"
    "     'search_text': 'FY2025 EBITDA of $412M, up 9% year over year on route density gains.'},\n"
    "    {'slide_id': 'nw-ic-03', 'deck_id': 'nw-ic', 'project': 'Northwind', 'deck_stage': 'Final IC', 'title': 'Market Overview', 'slide_type': 'market',\n"
    "     'search_text': 'Revenue grew to $3.1B on higher freight volumes; top 3 customers are 22% of sales.'},\n"
    "    {'slide_id': 'bw-ic-09', 'deck_id': 'bw-ic', 'project': 'Brightwater', 'deck_stage': 'Final IC', 'title': 'Historical Financials', 'slide_type': 'financials',\n"
    "     'search_text': 'Earnings before interest, taxes, depreciation and amortization reached $188M in 2025.'},\n"
    "    {'slide_id': 'bw-ic-12', 'deck_id': 'bw-ic', 'project': 'Brightwater', 'deck_stage': 'Final IC', 'title': 'Operations', 'slide_type': 'operations',\n"
    "     'search_text': 'Cut 200 jobs after closing the Ohio bottling plant; consolidated to two sites.'},\n"
    "    {'slide_id': 'ks-ic-06', 'deck_id': 'ks-ic', 'project': 'Kestrel', 'deck_stage': 'Final IC', 'title': 'Margin Profile', 'slide_type': 'financials',\n"
    "     'search_text': 'Adjusted EBITDA margin expanded to 31% as cloud hosting costs fell.'},\n"
    "    {'slide_id': 'ks-ic-08', 'deck_id': 'ks-ic', 'project': 'Kestrel', 'deck_stage': 'Final IC', 'title': 'Income Statement', 'slide_type': 'financials',\n"
    "     'search_text': 'Net income was $57M after a one-time tax charge.'},\n"
    "    {'slide_id': 'hc-ic-05', 'deck_id': 'hc-ic', 'project': 'Halcyon', 'deck_stage': 'Final IC', 'title': 'Financial Summary', 'slide_type': 'financials',\n"
    "     'search_text': 'Operating profit before D&A came in at $95M for the year.'},\n"
    "    {'slide_id': 'hc-ic-02', 'deck_id': 'hc-ic', 'project': 'Halcyon', 'deck_stage': 'Final IC', 'title': 'Investment Thesis', 'slide_type': 'thesis',\n"
    "     'search_text': 'Opened 14 new clinics and hired 600 nurses; de novo clinics break even in 18 months.'},\n"
    "    {'slide_id': 'ic-ic-04', 'deck_id': 'ic-ic', 'project': 'Ironclad', 'deck_stage': 'Final IC', 'title': 'Financial Summary', 'slide_type': 'financials',\n"
    "     'search_text': 'EBITDA fell to $640M as copper prices dropped.'},\n"
    "    {'slide_id': 'ic-ic-10', 'deck_id': 'ic-ic', 'project': 'Ironclad', 'deck_stage': 'Final IC', 'title': 'Capital Structure', 'slide_type': 'capital_structure',\n"
    "     'search_text': 'Paid down $300M of debt, cutting interest expense by a third.'},\n"
    ']\n'
    "EBITDA_SLIDES = {'nw-ic-07', 'bw-ic-09', 'ks-ic-06', 'hc-ic-05', 'ic-ic-04'}  # the right answers, marked * below\n"
    '\n'
    "S_text = np.array(list(model.passage_embed([s['search_text'] for s in slides])))  # embed the slide words only\n"
    '\n'
    'def rank(S, query, where=None, k=5):\n'
    '    """Rank slides by similarity to query. where = optional metadata filter, e.g. {\'project\': \'Halcyon\'}."""\n'
    '    q = np.array(list(model.query_embed(query)))[0]                      # embed the query\n'
    '    keep = [i for i, s in enumerate(slides)                              # metadata filter happens BEFORE ranking\n'
    '            if all(s[f] == v for f, v in (where or {}).items())]\n'
    '    keep.sort(key=lambda i: -(S[i] @ q))                                 # highest similarity first\n'
    "    print(query + (f'   (filter: {where})' if where else ''))\n"
    '    for i in keep[:k]:\n'
    '        s = slides[i]\n'
    "        star = '*' if s['slide_id'] in EBITDA_SLIDES else ' '\n"
    "        print(f\"  {S[i] @ q:.2f} {star} {s['project']:<12} {s['search_text'][:62]}\")\n"
    '\n'
    "rank(S_text, 'EBITDA')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- The three slides that literally say "EBITDA" tie at the top. Brightwater (spelled out) and Halcyon '
    '("operating profit before D&A") report the same metric but score much lower.\n'
    '- For this model the acronym acts more like a keyword than a concept. It doesn\'t reliably know '
    '"EBITDA" = "earnings before interest, taxes, depreciation and amortization". Small models and finance jargon are a weak pairing.\n'
    '- If a RAG system took the top 3, two of the five companies would silently be missing.\n'
))

cells.append(md(
    '### 5b · Asking about one company\n'
    '\n'
    'The slide text never names the company, so the embedding has no way to know which deal a slide belongs to.\n'
))

cells.append(code(
    "rank(S_text, 'Halcyon EBITDA')\n"
    "rank(S_text, 'Brightwater EBITDA')\n"
    "rank(S_text, 'What is the EBITDA of Ironclad?')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Both queries return the other companies\' EBITDA slides first. The company name in the query has nothing to match, '
    'so only the word "EBITDA" counts.\n'
    '- This is the normal case with slide decks: a "Financial Summary" slide rarely repeats the project name.\n'
    '- "What is the EBITDA of Ironclad?" gets the right slide first, but only just (0.59 vs 0.58 for Northwind). '
    'It wins because Ironclad\'s slide happens to be the shortest, most EBITDA-only text, not because the model matched "Ironclad". '
    'Reword the slide slightly and it could lose.\n'
    '- With a header line on each slide (5c) the same question wins clearly: 0.74 vs 0.60.\n'
))

cells.append(md(
    '### Is this viable? Embedding search vs RAG\n'
    '\n'
    'Everything so far is **search only**. Ask "What is the EBITDA of Ironclad?" and you get back a ranked list of slides, '
    'not the answer "$640M". RAG (topic 07) adds a second step: hand the top slides to an LLM and have it write the answer.\n'
    '\n'
    '| | Embedding search (this notebook) | RAG (search + LLM) |\n'
    '|---|---|---|\n'
    '| Output | ranked slides + similarity scores | a written answer, e.g. "Ironclad EBITDA was $640M (slide ic-ic-04)" |\n'
    '| Reads the text? | no, only compares vectors | yes, the LLM reads the retrieved slides |\n'
    '| Pulls out the number | no | yes |\n'
    '| Knows "operating profit before D&A" is EBITDA | weakly (this small model mostly doesn\'t) | yes, if that slide was retrieved |\n'
    '| "Not found" | never; always returns k slides, relevant or not | can say the slides don\'t contain the answer |\n'
    '| Compares numbers ("highest EBITDA") | no | only across the slides it was given |\n'
    '| Cost per question | one small embedding, ~free | embedding + an LLM call |\n'
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- For "What is X\'s EBITDA?" search alone is viable as a **finder**: a person looks at the top slide and reads the number. '
    'It is not viable as an **answerer**.\n'
    '- RAG is only as good as its retrieval. The LLM can only use the slides it is handed. If "Halcyon EBITDA" retrieves '
    'Ironclad\'s slide, the LLM either says "not found" or, worse, reports $640M as Halcyon\'s. That\'s why 5c-5d matter.\n'
    '- So show the LLM the metadata too, not just `search_text`. A slide labeled "Ironclad | Final IC | Financial Summary" '
    'lets it notice the mismatch; a bare "EBITDA fell to $640M" doesn\'t.\n'
    '- The LLM step also fixes some of what embeddings miss: it knows "operating profit before D&A" and "earnings before '
    'interest, taxes..." are EBITDA, as long as those slides make it into the top k. Retrieving more slides (k=10-20) helps here.\n'
))

cells.append(md(
    '### 5c · Fix 1: put the metadata into the text before embedding\n'
    '\n'
    'Prefix each slide with its project, deck stage and title, then embed that. The stored `search_text` doesn\'t change; '
    'only the text sent to the embedding model does.\n'
))

cells.append(code(
    'def with_context(s):\n'
    "    return f\"{s['project']} | {s['deck_stage']} | {s['title']}\\n{s['search_text']}\"   # header line + slide words\n"
    '\n'
    "print(with_context(slides[6]))\n"
    'print()\n'
    'S_ctx = np.array(list(model.passage_embed([with_context(s) for s in slides])))  # re-embed with the header\n'
    '\n'
    "rank(S_ctx, 'Halcyon EBITDA')\n"
    "rank(S_ctx, 'Brightwater EBITDA')\n"
    "rank(S_ctx, 'What is the EBITDA of Ironclad?')\n"
    "rank(S_ctx, 'EBITDA')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- "Brightwater EBITDA" goes from not in the top 5 to **#1**. "Halcyon EBITDA" improves (4th to 3rd) but still isn\'t first.\n'
    '- Plain "EBITDA" gets no better (Brightwater even drops out of the top 5): the header adds the company, '
    'not the meaning of the acronym.\n'
    '- Cheap and almost always worth doing. Re-embedding is needed whenever the header format changes.\n'
))

cells.append(md(
    '### 5d · Fix 2: filter on metadata, then rank\n'
))

cells.append(code(
    "rank(S_text, 'EBITDA', where={'project': 'Halcyon'})\n"
    "rank(S_text, 'EBITDA', where={'project': 'Brightwater'})\n"
    "rank(S_ctx,  'EBITDA', where={'slide_type': 'financials'}, k=6)\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Filtering by project finds the right slide every time, even with the weak text-only embeddings. '
    'When you know the project, filter on it; don\'t make the embedding guess.\n'
    '- `slide_type` narrows to financial slides, but the net income slide is still in there and still ranks above two real EBITDA slides. '
    'Filters shrink the haystack; they don\'t fix ranking.\n'
    '- In a real app an LLM reads the question ("EBITDA at underwriting for Project Surf"), pulls out '
    '`project=Surf`, `deck_stage=Final IC`, and passes them as filters. Vector databases (topic 04) support this directly.\n'
))

cells.append(md(
    '### 5e · Comparing numbers\n'
))

cells.append(code(
    "rank(S_ctx, 'which company has the highest EBITDA', k=4)\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Embeddings can\'t compare numbers. Northwind ($412M) ranks above Ironclad ($640M): '
    'the score reflects wording, not dollar amounts.\n'
    '- Questions like "highest", "over $50M" or "average multiple" need the numbers pulled into a table and answered with code or SQL.\n'
    '- Still open after both fixes: the acronym problem. Next steps in later topics: keyword search for exact terms (08 hybrid search), '
    'reranking (09), standardising metric names when extracting, or a bigger or finance-tuned embedding model.\n'
))

# --- 6. Long slides and tables -----------------------------------------------

cells.append(md(
    '## 6 · Two traps for deck data: long slides and tables\n'
))

cells.append(md(
    '### 6a · Long text gets cut off\n'
    '\n'
    'This model reads at most **512 tokens**. Anything after that is silently dropped. Here the EBITDA fact sits at the '
    '**end** of a slide, after more and more filler text.\n'
))

cells.append(code(
    'tok = model.model.tokenizer                                   # the embedding model\'s own tokenizer (not tiktoken)\n'
    "fact = 'Ironclad Mining FY2025 EBITDA was $640M.'\n"
    "filler = 'The committee reviewed site visits, management interviews, and customer references during diligence. '\n"
    "q = np.array(list(model.query_embed('Ironclad EBITDA')))[0]\n"
    '\n'
    "print(f\"{'filler sentences':>17}{'tokens seen':>13}{'score':>7}\")\n"
    'for n in (0, 5, 20, 40, 60):\n'
    '    text = filler * n + fact                                  # fact always at the very end\n'
    '    n_tok = len(tok.encode(text).ids)                         # tokens the model actually reads (capped at 512)\n'
    '    v = np.array(list(model.passage_embed([text])))[0]\n'
    "    print(f'{n:>17}{n_tok:>13}{float(v @ q):>7.3f}')\n"
    '\n'
    'only_filler = np.array(list(model.passage_embed([filler * 40])))[0]   # same text with NO fact at all\n'
    "print(f'\\n40 filler sentences, no fact at all:    score {float(only_filler @ q):.3f}')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- From 40 filler sentences on, the token count is stuck at 512 and the score stops changing: the fact has been cut off. '
    'The vector is identical to the one for filler with no fact at all. No error, no warning.\n'
    '- Even within the limit, extra text **dilutes** the fact (0.76 to ~0.65). One vector has to represent everything on the slide, '
    'so a single number on a busy slide counts for less.\n'
    '- For the real decks: measure how many `search_text` blobs exceed the limit. If many do, split long slides (topic 06) '
    'or use a model with a longer limit (many accept 8k+ tokens).\n'
))

cells.append(md(
    '### 6b · Tables: the labels matter, not the numbers\n'
    '\n'
    'The same EBITDA fact three ways: as a sentence, as a flattened table with its labels, and as a table that lost '
    'its labels (which can happen when converting PPTX to text). Plus an unrelated Ironclad slide for comparison.\n'
))

cells.append(code(
    'versions = {\n'
    "    'sentence':        'Ironclad Mining EBITDA was $640M in FY2025, down from $810M in FY2024.',\n"
    "    'table w/ labels': 'Ironclad Mining | FY2023 | FY2024 | FY2025\\nRevenue | 2,950 | 3,400 | 2,710\\n'\n"
    "                       'EBITDA | 720 | 810 | 640\\nCapex | 410 | 455 | 390\\nNet debt | 1,900 | 1,750 | 1,450',\n"
    "    'table no labels': 'FY2023 | FY2024 | FY2025\\n2,950 | 3,400 | 2,710\\n720 | 810 | 640\\n410 | 455 | 390',\n"
    "    'unrelated slide': 'Ironclad Mining paid down $300M of debt, cutting interest expense by a third.',\n"
    '}\n'
    'V = np.array(list(model.passage_embed(list(versions.values()))))\n'
    '\n'
    "queries = ['Ironclad EBITDA', 'Ironclad EBITDA FY2025', 'Ironclad revenue trend']\n"
    "print(' ' * 17 + ''.join(f'{q:>25}' for q in queries))\n"
    'Q = np.array([list(model.query_embed(q))[0] for q in queries])\n'
    'for name, row in zip(versions, V @ Q.T):                     # one row of scores per version\n'
    "    print(f'{name:<17}' + ''.join(f'{x:>25.2f}' for x in row))\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- A table that keeps its labels ("Ironclad Mining", "EBITDA", "Revenue") scores close to the sentence, and even beats it for '
    '"revenue trend". Flattened tables are fine **if the labels survive**.\n'
    '- Without labels, the same numbers score below an unrelated debt slide for two of the three queries. They only do OK on '
    '"FY2025", the one label the table kept. Embeddings match words; "720 | 810 | 640" has nothing to match.\n'
    '- For the real decks: spot-check how tables came out of the PPTX conversion. If row/column labels are missing or scrambled, '
    'fix the conversion (or have Claude rewrite each table with labels) before embedding anything.\n'
))

# --- 7. Size and cost --------------------------------------------------------

cells.append(md(
    '## 7 · Storage adds up\n'
))

cells.append(code(
    "print(f\"{'dims':>6}{'bytes/vec':>11}{'1M vectors':>13}\")\n"
    'for dims in (384, 1024, 1536, 3072):\n'
    '    b = dims * 4   # float32\n'
    "    print(f'{dims:>6}{b:>11,}{b * 1_000_000 / 1e9:>10.1f} GB')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Each vector is dims x 4 bytes (float32). A million 1536-dim vectors is ~6 GB before any index overhead.\n'
    '- Bigger vectors aren\'t always better. Smaller models are faster and cheaper; test on your own data. '
    'The MTEB leaderboard is the usual starting point for picking one.\n'
    '- Vectors from different models (or versions) live in different spaces and can\'t be compared. '
    'Change model = re-embed everything.\n'
    '- Anthropic doesn\'t offer an embedding model; its docs point to Voyage AI. Open models (like this one) run locally for free.\n'
))

cells.append(md(
    '## Gotchas\n'
    '\n'
    '- Acronyms vs spelled-out terms (EBITDA) don\'t reliably match with a small model (5a).\n'
    '- Slide text rarely names the company: add a metadata header before embedding, filter when you can (5b-5d).\n'
    '- Search finds slides; it doesn\'t answer, compare numbers or say "not found". That\'s the LLM step in RAG (5b, 5e).\n'
    '- Text past the model\'s token limit (512 here) is silently dropped (6a).\n'
    '- Tables only embed well if their row/column labels survive the text conversion (6b).\n'
    '- Different embedding models (or versions) can\'t be mixed; change model = re-embed everything (7).\n'
))

cells.append(md(
    '## Resources\n'
    '\n'
    '- \n'
))

if __name__ == "__main__":
    build("03_embeddings", cells)
