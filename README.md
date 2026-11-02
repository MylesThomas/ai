# ai

Notes + runnable code for 23 AI engineering concepts (tokens → LLMOps).

Each topic has a build script that generates a notebook and an HTML export:

```
src/ai_concepts/notebooks/build_01_tokens.py  ->  01_tokens.ipynb + 01_tokens.html (same folder)
```

**Take notes in the build scripts, not the `.ipynb`.** Notebooks are regenerated (see `RULES.md`).

## Usage

```
uv sync
uv run python src/ai_concepts/notebooks/build_07_rag.py      # one topic
uv run python src/ai_concepts/notebooks/build_all.py         # all topics
uv run python src/ai_concepts/notebooks/build_all.py 07 12   # a subset
uv run jupyter lab src/ai_concepts/notebooks/                               # scratch-run interactively
```

## Topics

| # | Topic | # | Topic |
|---|---|---|---|
| 01 | Tokens | 13 | AI agents |
| 02 | Context windows | 14 | Agentic workflows |
| 03 | Embeddings | 15 | LangGraph |
| 04 | Vector databases | 16 | LangChain |
| 05 | Semantic search | 17 | MCP |
| 06 | Chunking | 18 | Agent memory |
| 07 | RAG | 19 | LLM evaluations |
| 08 | Hybrid search | 20 | Ragas |
| 09 | Reranking | 21 | Guardrails |
| 10 | Loop engineering | 22 | LLM observability |
| 11 | Structured outputs | 23 | LLMOps |
| 12 | Function calling | | |
