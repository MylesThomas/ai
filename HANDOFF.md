# Handoff

**Pick up at 04 and 04b.** Both notebooks are written and build cleanly, but haven't been reviewed yet. Start by reading
through them (`src/ai_concepts/notebooks/04_vector_databases.html`, `04b_duckdb.html`) and adjusting before moving on to 05.

```
uv run python src/ai_concepts/data/fake_decks.py                # regenerate fake deck data (data/*.jsonl)
uv run python src/ai_concepts/notebooks/build_all.py 04 04b      # rebuild both notebooks
```

## Where things stand

| Topic | Status |
|---|---|
| 01 Tokens | Done |
| 02 Context windows | Done |
| 03 Embeddings | Done |
| 04 Vector databases | Written, **needs review** |
| 04b DuckDB | Written, **needs review** |
| 05 Semantic search | Planned (see below), not started |

## Use case driving the notebooks

~250 investment committee decks, converted from PPTX to JSONL (one line per slide: `slide_id`, `deck_id`, `title`,
`slide_type`, ..., `search_text`). 1-2 new decks a week. Goal: a RAG "wiki" that answers questions like
"What was EBITDA at underwriting for Project Surf?" and "Compare deal 1 to 3 past waste deals."

From 04 on, notebooks use fake decks shaped like that data, from `src/ai_concepts/data/fake_decks.py`:
8 deals (4 in waste, including Project Surf), Screening + Final IC decks, plus a Surf Portfolio Review used as the "new deck this week".
Fields `project`, `company`, `sector`, `deck_stage`, `deck_date` are placeholders until the real field names are known.

Direction agreed in 04b: DuckDB as the single store (slides + embeddings + metrics table), with Claude using tools on top
(SQL for numbers, filtered search for text, reading whole decks). Postgres + pgvector only if a shared app needs writes or per-deal permissions.

## Loose ends

- **01 tiktoken note:** with an API key, Claude's exact count was 1.85x tiktoken's estimate (4,808 vs 2,601). Section 4's notes call
  tiktoken "a rough estimate"; update them, and consider using the exact count for the cost estimate when a key is set.
- **`.env` loading:** the build scripts don't read `.env`. Either load it in the shell (`set -a; . ./.env; set +a`) before building,
  or add `python-dotenv`.
- **Deferred items:** see `docs/deferred.md` (embedding model comparison for topic 19, checks to run on the real deck data).

## Plan for 05 Semantic search (discussed, not agreed)

Basic semantic search is already covered in 03-04b, so 05 goes beyond it:

1. A small test set (~20 questions with their correct slides) and recall@k, so every change gets a score.
2. Getting filters out of the question: exact matching for project names, plus a small Claude call ("at underwriting" -> Final IC).
3. Finding similar deals: average slide vectors per deck, embed a deal profile, or search slides then group by deal.
4. Query rewriting for jargon: expansion and HyDE, measured on the test set.
5. Detecting "no match" (e.g. a project that doesn't exist).

Open questions to answer before writing 05:

- In "compare deal 1 to past waste deals", is deal 1 a **new** deal (not yet in the database) or one already in there?
- Model for the per-question Claude calls in steps 2 and 4: Haiku 5.5 suggested (simple, cheap, runs on every question).
- Keep all five sections, or keep 1-3 and move 4-5 into 08/09?
