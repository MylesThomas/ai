"""Shared helpers for build_XX_*.py scripts: cell constructors + write/execute/export."""

import logging
import sys
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor

PROJECT_ROOT = Path(__file__).resolve().parents[3]
NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"
LOG_DIR = PROJECT_ROOT / "src/ai_concepts/logs"

log = logging.getLogger("nb")


def setup_logging(name: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-7s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOG_DIR / (name + ".log"), mode="w", encoding="utf-8"),
        ],
        force=True,
    )


def md(source: str) -> nbformat.NotebookNode:
    return nbformat.v4.new_markdown_cell(source)


def code(source: str) -> nbformat.NotebookNode:
    return nbformat.v4.new_code_cell(source)


def build(name: str, cells: list, execute: bool = True, timeout: int = 600) -> None:
    """Write notebooks/<name>.ipynb, optionally execute it, and export notebooks/<name>.html."""
    setup_logging("build_" + name)
    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    nb_path = NOTEBOOK_DIR / (name + ".ipynb")
    html_path = NOTEBOOK_DIR / (name + ".html")

    nb = nbformat.v4.new_notebook()
    nb.cells = cells
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    n_code = sum(c.cell_type == "code" for c in cells)
    log.info("Built %s: %d cells (%d code, %d markdown)", name, len(cells), n_code, len(cells) - n_code)

    if execute:
        log.info("Executing %s (timeout=%ds per cell)", name, timeout)
        ExecutePreprocessor(timeout=timeout, kernel_name="python3").preprocess(
            nb, {"metadata": {"path": str(NOTEBOOK_DIR)}}
        )
        log.info("Execution finished")
    else:
        log.info("Skipping execution")

    nbformat.write(nb, nb_path)
    log.info("Wrote %s", nb_path.relative_to(PROJECT_ROOT))

    body, _ = HTMLExporter().from_notebook_node(nb)
    html_path.write_text(body, encoding="utf-8")
    log.info("Wrote %s (%d KB)", html_path.relative_to(PROJECT_ROOT), len(body) // 1024)
