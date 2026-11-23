# ssg

A small static site generator in Python. It turns Markdown files in `content/` into HTML pages using `template.html`, copies `static/` alongside, and writes everything to `docs/` (ready for GitHub Pages).

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

No third-party runtime dependencies.

## Usage

```sh
# Build for local use (links rooted at "/")
uv run src/main.py

# Build for GitHub Pages under /ssg/
./build.sh

# Preview the output
cd docs && python3 -m http.server 8888
```

`docs/` is wiped and regenerated on every build.

## Content

- Put Markdown in `content/`; the directory tree is mirrored into `docs/` (`foo.md` becomes `foo.html`).
- Each file must start with a `# Title` line. It becomes the page `<title>`.
- Supported syntax: headings, paragraphs, bold (`**`), italic (`_`), inline code, fenced code blocks, quotes, ordered and unordered lists, links, images.
- Put CSS and images in `static/`; reference them with absolute paths such as `/index.css`. A basepath argument rewrites them.

## Tests

```sh
./test.sh
```

## Layout

```
content/    Markdown source
static/     Files copied as-is
template.html   Page template ({{ Title }}, {{ Content }})
src/        Generator code and tests
docs/       Generated site (committed)
```
