# Initial Capabilities Overview

This report summarizes what the freshly cloned CLI can do today without the large language model (LLM) helper, and which features currently depend on the LLM pipeline.

## Programmatic Actions (Argument-Driven)

These commands run solely on CLI arguments/options and direct Notion API calls. They can be composed in scripts without any natural‑language processing.

- **Authentication**
  - `notion auth setup --token …` — stores the integration token and validates the connection (`src/notion_cli/main.py:81`).
  - `notion auth test` — pings the Notion API to confirm credentials (`src/notion_cli/main.py:106`).
- **Database utilities**
  - `notion db list` — lists all databases with IDs/URLs (`src/notion_cli/main.py:125`).
  - `notion db set-default <name>` / `notion db get-default` — manage the CLI default database (`src/notion_cli/main.py:166`, `src/notion_cli/main.py:195`).
  - `notion db show [name]` — tabular display with optional `--limit`, `--columns`, `--filter`, and `--save-view` flags (`src/notion_cli/main.py:211`). Filters are parsed by `FilterParser` and mapped to Notion JSON with `NotionFilterConverter` (`src/notion_cli/filters.py:24`, `src/notion_cli/filters.py:292`).
  - `notion db link` — prints database URL/ID, with optional clipboard copy (`src/notion_cli/main.py:1063`).
  - `notion db entry-link <entry>` — finds entries via fuzzy/exact match and returns their URLs (`src/notion_cli/main.py:1124`).
- **Saved views**
  - `notion view list` / `set-default` / `get-default` — manage saved view metadata (`src/notion_cli/main.py:470`, `src/notion_cli/main.py:508`, `src/notion_cli/main.py:532`).
  - `notion view show [name]` — replays a saved combination of columns, filters, and limits using the argument-driven `db show` under the hood (`src/notion_cli/main.py:548`).
  - `notion view delete` / `update` — remove or modify saved views (`src/notion_cli/main.py:586`, `src/notion_cli/main.py:605`), persisted via `ViewsManager` (`src/notion_cli/views.py:10`).
- **Page management**
  - `notion page list` / `find` — search pages with optional exact matching and result limits (`src/notion_cli/main.py:1269`, `src/notion_cli/main.py:1302`).
  - `notion page create <file.md>` — converts Markdown to Notion blocks and creates a page, optionally under a chosen parent via `--parent-name`/`--parent-id` (`src/notion_cli/main.py:1361`).
  - `notion page link` — shows (and optionally copies) private/public URLs (`src/notion_cli/main.py:1482`).
- **Shell completions**
  - `notion completion install|show|uninstall <shell>` — manages manual completion scripts for bash/zsh/fish/PowerShell (`src/notion_cli/main.py:1738`).
- **Miscellaneous**
  - `notion version` — prints the CLI version string (`src/notion_cli/main.py:1942`).

## LLM-Dependent Actions

These commands call the LLM service (`src/notion_cli/llm.py`) to interpret natural-language prompts. They cannot currently be driven purely through flags or structured arguments.

- `notion db create "<prompt>"` — generates structured database properties and optional file uploads from a natural-language description before creating a page (`src/notion_cli/main.py:721`).
- `notion db edit "<prompt>"` — uses the LLM to derive both the filter expression and the property updates to apply to matching entries (`src/notion_cli/main.py:861`).

Extending the CLI with additional argument-driven options would require adding new flags/handlers to these LLM-flavored commands or introducing parallel programmatic subcommands.
