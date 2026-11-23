# Repository Guidelines

## Project Overview
Python static site generator (boot.dev-style). Converts Markdown in `content/` to HTML via `template.html`, copies `static/`, outputs to `docs/` (served by GitHub Pages). No third-party runtime deps.

## Architecture & Data Flow
`src/main.py` → `copy_files_to_dir(static → docs)` (wipes `docs/` first!) → `generate_pages_recursive(content → docs)`.

Per page (`src/generator.py`): read md → `markdown_to_html_node` → `.to_html()` → `extract_title` → substitute `{{ Title }}` / `{{ Content }}` in the template → if basepath ≠ `/`, rewrite `href="/` and `src="/` to the basepath → write `index.html`-style path (`foo.md` → `foo.html`, dirs mirrored).

Markdown pipeline (`src/markdown/`):
- `parser.py`: block splitting (`\n\n`), `block_to_block_type`, regex extractors for images/links, `extract_title` (requires the file to START with `# `; raises otherwise).
- `splitter.py`: `text_to_textnodes` chains `split_nodes_delimiter` (bold/italic/code), image and link splitters. Only `TextType.TEXT` nodes get split further.
- `converter.py`: one `*_to_html_node` per `BlockType`, dispatched in `block_to_html_node`; root is `<div>`.
- `nodes/`: `HTMLNode` (dataclass) → `LeafNode` / `ParentNode`; `TextNode` + `text_node_to_html_node`.
- `enums/`: `BlockType`, `TextType`.

## Key Directories
- `src/` – all code; imports are relative to `src` (e.g. `from markdown.parser import ...`), NOT `src.`.
- `src/tests/` – unittest suite.
- `content/` – markdown input (`blog/<slug>/index.md`, `contact/`, `index.md`).
- `static/` – css/images copied verbatim.
- `docs/` – GENERATED output, committed for Pages. Never hand-edit.
- `public/` – dev output dir referenced by `main.sh` (gitignored/not present); note `config.py` `OUTPUT_DIR` is `docs`.

## Development Commands
- Prod build (basepath `/ssg/`): `./build.sh` → `uv run src/main.py "/ssg/"`
- Local build: `uv run src/main.py` (basepath `/`)
- Tests: `./test.sh` → `uv run python -m unittest discover -s src`
- Single test: `uv run python -m unittest discover -s src -p "test_textnode.py"`
- No linter/formatter configured. `main.sh` serves `public/` on :8888 (stale vs. `docs/`; serve with `cd docs && python3 -m http.server 8888`).

## Code Conventions & Common Patterns
- Type hints on signatures; `snake_case` functions, `PascalCase` classes, one module per concern.
- Pure functions returning new lists of nodes (no mutation); splitters pass through non-`TEXT` nodes.
- Errors: plain `Exception`/`ValueError` with message (e.g. "delimiter not closed", "No header found").
- Markdown-to-HTML functions named `<block>_to_html_node`; tests named `test_<module/function>.py`.
- Template placeholders are literal strings `{{ Title }}`/`{{ Content }}` (exact spacing); no templating lib.
- Absolute URLs in content/template (`/index.css`, `/images/x.png`) rely on basepath rewrite.
- Module-level `main()` call in `main.py` (no `__main__` guard); importing it runs the build.

## Important Files
`src/main.py`, `src/generator.py`, `src/config.py` (paths), `template.html`, `build.sh`, `test.sh`, `pyproject.toml`, `uv.lock`.

## Runtime/Tooling Preferences
Python 3.11 (`.python-version`), `uv` as runner/package manager. Run from repo root (paths in `config.py` are relative). Stdlib only; don't add deps without need.

## Testing & QA
stdlib `unittest`, files in `src/tests/test_*.py`, tests import like source (`from nodes.textnode import ...`) so run via discover with `-s src`. After changing content/generator, rebuild with `./build.sh` and commit updated `docs/`. No coverage requirement.
