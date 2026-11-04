# Deferred items

Things we noticed while working through the topics but chose to cover later. Each entry says where it came up,
why it matters for the investment committee deck use case, and which topic should pick it up.

Use case for context: ~250 investment committee decks, converted from PPTX to JSONL (one line per slide:
`slide_id`, `deck_id`, `title`, `slide_type`, ..., `search_text`). Goal is a RAG "wiki" that answers questions like
"What was EBITDA at underwriting for Project Surf?" and "Compare deal 1 to 3 past waste deals."

---

## Compare embedding models on the EBITDA test

- **Found in:** 03 Embeddings, section 5a.
- **What we saw:** the small local model (`BAAI/bge-small-en-v1.5`, 384 dims) treats "EBITDA" more like a keyword
  than a concept. Slides that say "earnings before interest, taxes, depreciation and amortization" or "operating
  profit before D&A" rank below a net income slide when searching "EBITDA".
- **Why deferred:** we don't know yet whether this is a small-model problem or an embeddings problem in general.
  Answering that needs a proper side-by-side on the same slides and queries, which is what evaluations are for.
- **To do:** run the 03 section 5 slides and queries against a larger local model (e.g. bge-large) and a
  finance-tuned API model (e.g. Voyage's finance model). Measure whether the spelled-out and synonym slides make the top k.
  Weigh the result against cost, and against whether the decks can be sent to an external API.
- **Pick up in:** 19 LLM evaluations.

## 2D plot of the embeddings

- **Found in:** 03 Embeddings.
- **What it is:** project the vectors down to 2D (PCA or UMAP) and plot them, so clusters by company or by slide type are visible.
- **Why deferred:** good for intuition, but it doesn't change any design decision for the deck use case.
- **Pick up in:** optional. 05 Semantic search if there is time, once there is a larger fake deck corpus to plot.

---

## Checks to run on the real deck data

These came out of 03 and only matter once we have the real JSONL in hand.

- **Slide length vs the embedding model's token limit** (03 section 6a). The current model reads 512 tokens and silently
  drops the rest. Measure what share of `search_text` blobs go over. That decides the chunking strategy (06) or the model choice.
- **Table quality after the PPTX-to-text conversion** (03 section 6b). Tables embed fine if their row/column labels
  survive, and badly if they don't. Spot-check several financials slides for intact labels before embedding.
- **Real metadata field names** (03 section 5). The notebook uses placeholder fields `project` and `deck_stage`. Find
  what the real data uses for project/code name, deck stage (screening / final IC / portfolio review) and date,
  and whether they are on each slide or only per deck.
- **Confidentiality** (discussed during 03). Confirm the decks can be sent to the Claude API (and to any external
  embedding API), and under what data retention terms. If not, everything has to run locally.
