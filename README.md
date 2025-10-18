# Notion CLI

[![PyPI version](https://badge.fury.io/py/notion-cli.svg)](https://badge.fury.io/py/notion-cli)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

AI-powered CLI tool for managing Notion databases with natural language commands.

## Quick Start

### Installation

```bash
pip install notion-cli
```

### Setup

1. **Create a Notion Integration** at [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. **Authenticate:**
   ```bash
   notion auth setup --token <your-integration-token>
   ```

### Basic Usage

```bash
# List databases
notion db list

# Set default database
notion db set-default "Tasks"

# View entries
notion db show
notion db show "Tasks" --limit 5

# Create with AI (natural language)
notion db create "Add high priority task to review reports due Friday"

# Edit with AI
notion db edit "Mark all completed tasks as archived"

# Filter entries
notion db show --filter "Status=Done"
notion db show --filter "Priority=High AND Status!=Archived"

# View with custom columns
notion db show --columns "Name,Status,Priority"

# Get entry link
notion db entry-link "Tasks" "meeting"

# Create pages
notion page create --file "spec.md" --parent-name "Projects"

# Find pages
notion page find "Meeting Notes"

# Machine-readable JSON output
notion db list --json
notion db show "Tasks" --json | jq '.entries[] | {name: .properties.Name, status: .properties.Status}'
```

## Key Features

- **🧠 AI-powered** - Natural language to create/edit database entries
- **📊 JSON output** - All commands support `--json` for scripting
- **🎯 Defaults** - Set default database/view to reduce typing
- **🔍 Prefix matching** - Use partial names with auto-completion
- **🔗 Clickable links** - Terminal-friendly database and entry URLs
- **📝 Page management** - Create, update, and search pages
- **💾 Saved views** - Store filtered views for team workflows
- **🔑 Auto config** - API key prompts on first use

## Common Commands

| Command | Purpose |
|---------|---------|
| `notion auth setup` | Authenticate |
| `notion db list` | List all databases |
| `notion db show [name]` | View entries |
| `notion db create "prompt"` | Create entry with AI |
| `notion db edit "prompt"` | Edit entries with AI |
| `notion db set-default` | Set default database |
| `notion view show [name]` | Show saved view |
| `notion page create --file` | Create page |
| `notion page find "query"` | Search pages |

## Configuration

The CLI prompts for model selection and API key automatically on first use.

**Environment variables (optional):**
```bash
NOTION_TOKEN=ntn_...                  # Override config file
NOTION_CLI_LLM_MODEL=claude-3-sonnet  # Set model
```

**Supported models:** GPT-4, Claude, Gemini, and others via LiteLLM

## Documentation

- **Full examples** → See [examples/index.md](examples/index.md)
- **Help** → `notion --help`

## Setup & Development

```bash
# Install with uv
uv sync

# Run CLI
uv run notion db list

# Format & lint
uv run ruff format
uv run ruff check

# Type check
uv run mypy src/

# Tests
uv run pytest tests/

# Install pre-commit hooks
uv run pre-commit install
```

## License

MIT
