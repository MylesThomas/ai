"""Build 04b_duckdb.ipynb + .html (same folder). Edit notes here, never the .ipynb.

    uv run python src/ai_concepts/data/fake_decks.py              # once, writes data/fake_decks*.jsonl
    uv run python src/ai_concepts/notebooks/build_04b_duckdb.py
"""

from ai_concepts.notebooks._nb import build, code, md

cells = []

cells.append(md(
    '# 04b · DuckDB: one file instead of a vector database\n'
    '\n'
    '> For ~250 investment committee decks, a single DuckDB file can hold the slides, their embeddings and the metrics table, '
    'and answer questions a vector database can\'t.\n'
))

cells.append(md(
    '## Why this notebook exists\n'
    '\n'
    '- 04 showed what a vector database does. The use case here is small: ~250 decks, ~10k slides, 1-2 new decks a week, '
    'a few analysts asking questions.\n'
    '- At that size, exact search over every slide takes milliseconds (04 section 1), so an ANN index isn\'t needed. '
    'What *is* needed: saved to disk, metadata filters, updates, and a **metrics table** for questions like '
    '"EBITDA at underwriting" or "highest EBITDA" that similarity search can\'t answer (03 section 5e).\n'
    '- **DuckDB** is an in-process SQL database (like SQLite, built for analysis). One file, no server. '
    'It has a fixed-size array type for embeddings and a built-in cosine similarity function.\n'
))

cells.append(code(
    'import json\n'
    'import os\n'
    'import time\n'
    'import warnings\n'
    "warnings.filterwarnings('ignore', message='IProgress not found')   # harmless progress-bar warning\n"
    'from pathlib import Path\n'
    '\n'
    'import duckdb\n'
    'import numpy as np\n'
    'from fastembed import TextEmbedding\n'
    '\n'
    "DATA = Path.cwd().parents[2] / 'data'\n"
    "slides = [json.loads(line) for line in open(DATA / 'fake_decks.jsonl')]\n"
    "new_slides = [json.loads(line) for line in open(DATA / 'fake_decks_new.jsonl')]\n"
    "metrics = [json.loads(line) for line in open(DATA / 'fake_metrics.jsonl')]\n"
    "print(len(slides), 'slides,', len(new_slides), 'new slides,', len(metrics), 'metric rows')\n"
    '\n'
    "model = TextEmbedding('BAAI/bge-small-en-v1.5')\n"
    '\n'
    'def with_context(s):\n'
    "    return f\"{s['project']} | {s['deck_stage']} | {s['title']}\\n{s['search_text']}\"\n"
    '\n'
    'def show(sql, params=()):\n'
    '    """Run a query and print the result as an aligned table."""\n'
    '    cur = con.execute(sql, list(params))\n'
    '    cols = [d[0] for d in cur.description]\n'
    '    rows = [[f\'{v:.2f}\' if isinstance(v, float) else str(v) for v in r] for r in cur.fetchall()]\n'
    '    widths = [max(len(c), *(len(r[i]) for r in rows)) if rows else len(c) for i, c in enumerate(cols)]\n'
    "    print('  '.join(c.ljust(w) for c, w in zip(cols, widths)))\n"
    '    for r in rows:\n'
    "        print('  '.join(v.ljust(w) for v, w in zip(r, widths)))\n"
))

cells.append(md(
    '**About the metrics:** `fake_metrics.jsonl` stands in for what an extraction step would produce: Claude reads each deck '
    'and pulls out EBITDA, revenue, EV, entry multiple, MOIC and IRR, each with the label the deck used and the slide it came from '
    '(topic 11, structured outputs). Here they come from the same generator as the slides.\n'
))

# --- 1. Schema ---------------------------------------------------------------

cells.append(md(
    '## 1 · One file, three tables\n'
    '\n'
    '- `decks`: one row per deck (project, company, sector, stage, date)\n'
    '- `slides`: one row per slide, with the embedding stored as `FLOAT[384]`\n'
    '- `metrics`: one row per number per deck, with the slide it came from\n'
))

cells.append(code(
    "DB_PATH = DATA / 'decks_04b.duckdb'\n"
    'DB_PATH.unlink(missing_ok=True)                    # start fresh on every build\n'
    'con = duckdb.connect(str(DB_PATH))                 # the whole database is this one file\n'
    '\n'
    'SCHEMA = [\n'
    "    'CREATE TABLE decks (deck_id VARCHAR PRIMARY KEY, project VARCHAR, company VARCHAR, sector VARCHAR,'\n"
    "    '                    deck_stage VARCHAR, deck_date DATE)',\n"
    "    'CREATE TABLE slides (slide_id VARCHAR PRIMARY KEY, deck_id VARCHAR, slide_number INT, title VARCHAR,'\n"
    "    '                     slide_type VARCHAR, search_text VARCHAR, embedding FLOAT[384])',   # fixed-size array for vectors\n"
    "    'CREATE TABLE metrics (deck_id VARCHAR, metric VARCHAR, period VARCHAR, label_in_deck VARCHAR,'\n"
    "    '                      value DOUBLE, unit VARCHAR, source_slide_id VARCHAR)',\n"
    ']\n'
    'for stmt in SCHEMA:\n'
    '    con.execute(stmt)\n'
    '\n'
    'def ingest_deck(con, deck_slides, deck_metrics):\n'
    '    """Load one deck in a single transaction. Re-loading the same deck replaces it (safe to re-run)."""\n'
    "    deck_id = deck_slides[0]['deck_id']\n"
    '    vecs = list(model.passage_embed([with_context(s) for s in deck_slides]))\n'
    "    con.execute('BEGIN TRANSACTION')                 # all or nothing: readers never see half a deck\n"
    '    try:\n'
    "        for table in ('metrics', 'slides', 'decks'):\n"
    "            con.execute(f'DELETE FROM {table} WHERE deck_id = ?', [deck_id])   # remove any old copy\n"
    '        s0 = deck_slides[0]\n'
    "        con.execute('INSERT INTO decks VALUES (?, ?, ?, ?, ?, ?)',\n"
    "                    [deck_id, s0['project'], s0['company'], s0['sector'], s0['deck_stage'], s0['deck_date']])\n"
    "        con.executemany('INSERT INTO slides VALUES (?, ?, ?, ?, ?, ?, ?)',\n"
    "                        [[s['slide_id'], deck_id, s['slide_number'], s['title'], s['slide_type'], s['search_text'], v.tolist()]\n"
    '                         for s, v in zip(deck_slides, vecs)])\n'
    "        con.executemany('INSERT INTO metrics VALUES (?, ?, ?, ?, ?, ?, ?)',\n"
    "                        [[m['deck_id'], m['metric'], m['period'], m['label_in_deck'], m['value'], m['unit'], m['source_slide_id']]\n"
    '                         for m in deck_metrics])\n'
    "        con.execute('COMMIT')\n"
    '    except Exception:\n'
    "        con.execute('ROLLBACK')                       # leave the database exactly as it was\n"
    '        raise\n'
    '\n'
    'def by_deck(rows):\n'
    '    out = {}\n'
    '    for r in rows:\n'
    "        out.setdefault(r['deck_id'], []).append(r)\n"
    '    return out\n'
    '\n'
    't = time.perf_counter()\n'
    'slides_by_deck, metrics_by_deck = by_deck(slides), by_deck(metrics)\n'
    'for deck_id, deck_slides in slides_by_deck.items():\n'
    '    ingest_deck(con, deck_slides, metrics_by_deck.get(deck_id, []))\n'
    'load_s = time.perf_counter() - t\n'
    "print(f'loaded {len(slides_by_deck)} decks in {load_s:.1f}s (mostly embedding)')\n"
    "show('SELECT (SELECT count(*) FROM decks) AS decks, (SELECT count(*) FROM slides) AS slides, '\n"
    "     '(SELECT count(*) FROM metrics) AS metrics')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- The same `ingest_deck` function does the first load and every weekly update (section 5). One code path, tested every time.\n'
    '- The transaction means a reader never sees a half-loaded deck, and a crash mid-load leaves the old data intact.\n'
    '- Deck-level fields live once in `decks` instead of being copied onto every slide; queries join them back.\n'
))

# --- 2. Vector search in SQL -------------------------------------------------

cells.append(md(
    '## 2 · Vector search is just SQL\n'
    '\n'
    'Similarity is a function in the `SELECT`; filters are a normal `WHERE`. Same query as 04 section 3.\n'
))

cells.append(code(
    'def search(query, where=\'TRUE\', params=(), k=5):\n'
    '    """Exact similarity search over slides. where = any SQL condition on slides (s) or decks (d)."""\n'
    '    q = list(model.query_embed(query))[0].tolist()\n'
    "    print(query + ('' if where == 'TRUE' else f'   WHERE {where} {list(params)}'))\n"
    '    show(\n'
    "        'SELECT s.slide_id, d.deck_stage, '\n"
    "        '       round(array_cosine_similarity(s.embedding, ?::FLOAT[384])::DOUBLE, 2) AS score, '   # similarity per slide\n"
    "        '       left(replace(s.search_text, chr(10), \\' / \\'), 60) AS text '\n"
    "        'FROM slides s JOIN decks d USING (deck_id) '\n"
    "        'WHERE ' + where + ' '                                                                  # metadata filter\n"
    "        'ORDER BY score DESC LIMIT ' + str(k),\n"
    '        [q, *params])\n'
    '    print()\n'
    '\n'
    "search('What was EBITDA for Project Surf?')\n"
    "search('What was EBITDA for Project Surf?', \"d.project = ? AND d.deck_stage = 'Final IC'\", ['Surf'], k=3)\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Same ranking as Qdrant in 04 (screening deck on top unfiltered, Final IC once filtered). Same embeddings, same exact search, same answer.\n'
    '- Any SQL works as the filter: `IN (...)`, date ranges (`d.deck_date >= \'2023-01-01\'`), joins to other tables. '
    'A vector database supports only the filter types it was built with.\n'
))

# --- 3. Questions SQL answers ------------------------------------------------

cells.append(md(
    '## 3 · The questions similarity search couldn\'t answer\n'
    '\n'
    'These go to the metrics table, not the embeddings.\n'
))

cells.append(code(
    '# "What was EBITDA at underwriting for Project Surf?"\n'
    "show('SELECT d.deck_stage, d.deck_date, m.period, m.label_in_deck, m.value AS ebitda_musd, m.source_slide_id '\n"
    "     'FROM metrics m JOIN decks d USING (deck_id) '\n"
    "     \"WHERE d.project = 'Surf' AND m.metric = 'ebitda' AND d.deck_stage = 'Final IC'\")\n"
))

cells.append(code(
    '# "Which deal had the highest EBITDA at underwriting?"\n'
    "show('SELECT d.project, d.sector, m.label_in_deck, m.value AS ebitda_musd '\n"
    "     'FROM metrics m JOIN decks d USING (deck_id) '\n"
    "     \"WHERE m.metric = 'ebitda' AND d.deck_stage = 'Final IC' \"\n"
    "     'ORDER BY m.value DESC')\n"
))

cells.append(code(
    '# "Compare Surf to our past waste deals" -> one row per deal, same fields for each (at underwriting)\n'
    "show('PIVOT (SELECT d.project, d.deck_date, m.metric, m.value '\n"
    "     '       FROM metrics m JOIN decks d USING (deck_id) '\n"
    "     \"       WHERE d.sector = 'Waste' AND d.deck_stage = 'Final IC') \"\n"
    "     \"ON metric IN ('ebitda', 'revenue', 'ev', 'entry_multiple', 'moic', 'irr') USING first(value) \"   # one column per metric\n"
    "     'ORDER BY deck_date')\n"
))

cells.append(code(
    '# Mix both: similarity search, restricted by SQL to risk slides of waste deals at underwriting\n'
    "search('exposure to prices we do not control',\n"
    "       \"d.sector = 'Waste' AND d.deck_stage = 'Final IC' AND s.slide_type = 'risks'\", k=4)\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- "EBITDA at underwriting" is now a lookup with a citation (`source_slide_id`), not a similarity guess. '
    'The deck\'s own label is kept (`Adj. EBITDA`) so the answer can say which EBITDA it is.\n'
    '- "Highest" is an `ORDER BY`: Quarry ($58.4M) first. Similarity search ranked by wording, not dollars (03 section 5e).\n'
    '- The comparison table puts every waste deal on the same fields, whatever each deck called them '
    '(Granite\'s spelled-out EBITDA and Ember\'s "operating profit before D&A" are both just `ebitda` here). '
    'That\'s the payoff of extracting metrics once, up front.\n'
    '- The last query mixes both: SQL picks the slides (waste, underwriting, risks), similarity ranks them. '
    '"Prices we do not control" ranks commodity (Granite) and RIN credit (Ember) exposure first. Fuel (Surf) comes 4th, '
    'behind Harbor\'s facility outage, so "price" risks are found but not perfectly ranked.\n'
    '- In the full system Claude would choose between these: write SQL for numbers, call `search` for text (topics 12-13).\n'
))

# --- 4. Speed at realistic size ----------------------------------------------

cells.append(md(
    '## 4 · Is exact search fast enough?\n'
    '\n'
    '250 decks at ~40 slides each is ~10k slides. Timed on random vectors at that size and 10x larger.\n'
))

cells.append(code(
    "q = list(model.query_embed('EBITDA'))[0].tolist()\n"
    "print(f\"{'rows':>8}{'ms/query':>10}\")\n"
    'for n in (10_000, 100_000):\n'
    "    con.execute(f'CREATE OR REPLACE TEMP TABLE bench AS SELECT range AS id, '\n"
    "                f'list_transform(range(384), lambda x: random()::FLOAT)::FLOAT[384] AS embedding FROM range({n})')\n"
    '    runs = []\n'
    '    for _ in range(5):\n'
    '        t = time.perf_counter()\n'
    "        con.execute('SELECT id FROM bench ORDER BY array_cosine_similarity(embedding, ?::FLOAT[384]) DESC LIMIT 10', [q]).fetchall()\n"
    '        runs.append(time.perf_counter() - t)\n'
    "    print(f'{n:>8,}{min(runs) * 1000:>10.1f}')\n"
    "con.execute('DROP TABLE bench')\n"
    '\n'
    'per_slide = load_s / len(slides)\n'
    "print(f'\\nembedding + loading: {per_slide * 1000:.0f} ms/slide -> 10k slides in ~{per_slide * 10_000 / 60:.0f} min (one-time)')\n"
    "con.execute('CHECKPOINT')                          # flush pending writes into the main file before measuring\n"
    "print(f'database file: {DB_PATH.stat().st_size / 1e6:.1f} MB for {len(slides)} slides '\n"
    "      f'(includes fixed overhead; vectors alone are 1.5 KB/slide -> ~15 MB at 10k slides)')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- ~10k slides: about 10 ms per search, exact (recall 1.0, nothing missed). Even 100k is well under a tenth of a second.\n'
    '- The full corpus embeds in minutes on a laptop CPU, once. Weekly updates embed ~40 slides.\n'
    '- DuckDB does have an HNSW extension (`vss`) for larger data. Not needed here, and it was still marked experimental last we checked.\n'
))

# --- 5. Weekly update --------------------------------------------------------

cells.append(md(
    '## 5 · The weekly update\n'
    '\n'
    'This week the Surf **Portfolio Review** deck arrived. Same function as the initial load.\n'
))

cells.append(code(
    "pr_metrics = [m for m in metrics if m['deck_id'] == 'surf-pr']\n"
    'ingest_deck(con, new_slides, pr_metrics)\n'
    'ingest_deck(con, new_slides, pr_metrics)          # run it twice by mistake: no duplicates\n'
    '\n'
    "show('SELECT d.deck_stage, d.deck_date, m.label_in_deck, m.value AS ebitda_musd, m.source_slide_id '\n"
    "     'FROM metrics m JOIN decks d USING (deck_id) '\n"
    "     \"WHERE d.project = 'Surf' AND m.metric = 'ebitda' ORDER BY d.deck_date\")\n"
    "show('SELECT count(*) AS slides FROM slides')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- Surf\'s EBITDA history is one query: $38.0M at screening, $41.5M at underwriting, $44.2M actual in 2025. '
    'A question like "how has Surf done vs underwriting?" becomes easy to answer correctly.\n'
    '- The weekly job, in full: convert PPTX to JSONL, run extraction (Claude) on the new deck only, `ingest_deck`. Cents and a minute or two.\n'
    '- Older decks are kept on purpose. "At underwriting" questions need the Final IC numbers even after newer decks arrive.\n'
))

cells.append(md(
    '### Rebuild from scratch, then swap\n'
    '\n'
    'Keep the JSONL files as the source of truth, and be able to rebuild the whole database from them: after a schema change, '
    'a new embedding model, or a bad load. Build into a new file, then swap it in, so readers never see a half-built database.\n'
))

cells.append(code(
    'def rebuild(live_path, deck_files, metric_file):\n'
    '    """Build a complete new database file from JSONL, then replace the live file in one step."""\n'
    "    tmp_path = live_path.with_suffix('.tmp.duckdb')\n"
    '    tmp_path.unlink(missing_ok=True)\n'
    '    new_con = duckdb.connect(str(tmp_path))\n'
    '    for stmt in SCHEMA:\n'
    '        new_con.execute(stmt)\n'
    '    all_slides = [json.loads(line) for f in deck_files for line in open(f)]\n'
    '    all_metrics = by_deck(json.loads(line) for line in open(metric_file))\n'
    '    for deck_id, deck_slides in by_deck(all_slides).items():\n'
    '        ingest_deck(new_con, deck_slides, all_metrics.get(deck_id, []))\n'
    '    new_con.close()\n'
    '    os.replace(tmp_path, live_path)                 # atomic rename: old file -> new file in one step\n'
    '    return len(all_slides)\n'
    '\n'
    'con.close()                                        # readers must reopen after a swap\n'
    't = time.perf_counter()\n'
    "n = rebuild(DB_PATH, [DATA / 'fake_decks.jsonl', DATA / 'fake_decks_new.jsonl'], DATA / 'fake_metrics.jsonl')\n"
    "print(f'rebuilt {n} slides in {time.perf_counter() - t:.1f}s')\n"
    'con = duckdb.connect(str(DB_PATH), read_only=True)  # app side: read-only connection\n'
    "show('SELECT count(*) AS decks FROM decks')\n"
))

cells.append(md(
    '**Notes:**\n'
    '\n'
    '- On the real data, the expensive step in a rebuild is Claude extraction, not embedding. Cache extraction output per deck '
    '(e.g. one JSON file per deck) so a rebuild only re-embeds.\n'
    '- The app opens the file **read-only**. Several read-only processes can share one file; only the weekly job writes.\n'
    '- Backup = copy the file.\n'
))

# --- 6. Limits ---------------------------------------------------------------

cells.append(md(
    '## 6 · When DuckDB isn\'t enough\n'
    '\n'
    '| Limitation | Matters for the deck use case? |\n'
    '|---|---|\n'
    '| **One writer at a time.** In-process, not a server; many readers only in read-only mode | No: one weekly job writes, the app only reads. Yes if the app starts saving chats, feedback or notes from many users |\n'
    '| **ANN at millions of vectors** with filters (vector DBs filter during the HNSW search) | No: ~10k slides, exact search in ~10 ms |\n'
    '| **Very large scale** (sharding, replicas, billions of vectors) | No |\n'
    '| **Many small writes per second** (built for bulk loads and big queries) | No: 1-2 decks a week |\n'
    '| **Vector-only features**: quantization, multi-vector (ColBERT), built-in sparse+dense fusion and reranking | Not yet. Hybrid search (08) is doable in DuckDB with its full-text extension, scored in SQL |\n'
    '| **Users and permissions** (accounts, per-tenant access, audit) | Maybe: if some deals must be hidden from some people, enforce it in the app or move to Postgres |\n'
    '\n'
    '**Which apps need many small writes per second?** Payments, orders, messaging, logs, sensors, clickstream; and with vectors: '
    'chatbot memory saved every turn, recommendations updated on every click, news or tickets indexed the moment they arrive. '
    'Deck processing is the opposite pattern: occasional batch writes, then mostly reads.\n'
))

cells.append(md(
    '### Recommendation for ~250 decks, 1-2 new per week\n'
    '\n'
    '- **Use DuckDB** with the weekly batch job above, and keep JSONL + cached extraction as the source of truth.\n'
    '- **Move to Postgres + pgvector** if any of these happen: a shared web app that writes (saved chats, feedback); per-deal permissions '
    '(Postgres row-level security); several services writing at once. It keeps the same SQL, so the move is mostly mechanical.\n'
    '- **Consider a dedicated vector database** only at much larger scale or if one is already run by your team. '
    'For this use case it never comes up as the next step.\n'
))

cells.append(code(
    'con.close()\n'
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
    build("04b_duckdb", cells)
