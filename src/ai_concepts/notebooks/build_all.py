"""Run every build_XX_*.py in order.

    uv run python src/ai_concepts/notebooks/build_all.py          # all
    uv run python src/ai_concepts/notebooks/build_all.py 07 12    # just these
"""

import logging
import runpy
import sys
from pathlib import Path

from ai_concepts.notebooks._nb import setup_logging

HERE = Path(__file__).resolve().parent
log = logging.getLogger("build_all")


def main(only: list[str]) -> None:
    scripts = sorted(HERE.glob("build_[0-9][0-9]_*.py"))
    if only:
        scripts = [s for s in scripts if s.stem.split("_")[1] in only]
    failed = []
    for i, script in enumerate(scripts, 1):
        setup_logging("build_all")
        log.info("[%d/%d] %s", i, len(scripts), script.name)
        try:
            runpy.run_path(str(script), run_name="__main__")
        except Exception:
            setup_logging("build_all")
            log.exception("FAILED %s", script.name)
            failed.append(script.name)
    setup_logging("build_all")
    log.info("Done: %d built, %d failed %s", len(scripts) - len(failed), len(failed), failed or "")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
