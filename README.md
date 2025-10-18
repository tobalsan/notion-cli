# Notion CLI

[![PyPI version](https://badge.fury.io/py/notion-cli-ai.svg)](https://badge.fury.io/py/notion-cli-ai)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A command-line tool for managing Notion databases with AI-powered natural language entry creation.

## Quick Start

### Installation

```bash
pip install notion-cli-ai
```

### Setup

1. **Create a Notion Integration:**
   - Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
   - Create new integration and copy the token
   - Share your databases with the integration

2. **Authenticate:**
   ```bash
   notion auth setup --token <your-integration-token>
   ```

3. **Set up AI (optional):**
   - API keys will be prompted for automatically when needed

### Basic Usage

```bash
# List databases
notion db list

# Set default database to avoid typing it repeatedly
notion db set-default "Tasks"

# View database entries (uses default database if no name provided)
notion db show "Tasks"
notion db show  # Uses default database

# Create entry with AI (new improved syntax - prompt first)
notion db create "Add high priority task to review quarterly reports due Friday" --database "Tasks"
notion db create "Add high priority task to review quarterly reports due Friday"  # Uses default database

# Edit entries with AI (prompt first syntax)
notion db edit "Mark all completed tasks as archived" --database "Tasks"
notion db edit "Mark all completed tasks as archived"  # Uses default database

# Use prefix matching for database names
notion db show "Task"  # Matches "Tasks" automatically
notion db show "Pro"   # Shows selection menu if multiple matches like "Projects", "Proposals"

# Create pages in multiple ways
notion page create --file "path/to/file.md" --parent-name "My Workspace"
notion page create --parent-id "abc123" --properties '{"Name": "New Page", "Status": "Active"}'
notion page create --parent-name "Projects" --blocks '[...]' --properties '{"Name": "Task"}'

# Update existing pages
notion page update "Meeting Notes" --file "updated-notes.md"
notion page update --id "page-id" --properties '{"Status": "Complete"}'
notion page update "Design Doc" --blocks '[...]' --properties '{"Status": "Published"}'

# Get database/entry links (clickable in terminal)
notion db link "Tasks"
notion db entry-link "Tasks" "meeting"
```

## Key Features

- **🧠 AI-powered creation/editing** - Use natural language to create and update entries with improved filter generation
- **🎯 Default database/view support** - Set defaults to avoid typing database names repeatedly
- **🔍 Prefix matching** - Use partial database/view names with auto-completion and selection menus
- **🖱️ Clickable links** - Database and entry URLs are clickable in terminal output
- **🔑 Automatic API key management** - CLI prompts for missing keys and saves them
- **📊 JSON output mode** - All commands support `--json` flag for machine-readable output
- **Smart filtering** - `--filter "status=Done,priority=High"`
- **Custom columns** - `--columns "Name,Status,Priority"`
- **File uploads** - `--file resume.pdf`
- **Interactive mode** - `--interactive` to revise AI prompts
- **Shell completions** - `notion completion install bash`

## JSON Output

All commands support the `--json` flag for machine-readable output, perfect for scripting, automation, and integration with other tools:

```bash
# List databases as JSON
notion db list --json

# Get database entries as JSON
notion db show "Tasks" --json

# Pipe to jq for filtering
notion db list --json | jq '.databases[] | select(.title == "Tasks")'

# Filter and extract specific fields
notion db show "Tasks" --filter "Status=Done" --json | jq '.entries[] | {id, url}'

# Create entry and capture ID
ENTRY_ID=$(notion db create "New task" --json | jq -r '.entry_id')

# Get links programmatically
notion db link "Tasks" --json | jq -r '.url'
notion page find "Meeting Notes" --json | jq '.pages[] | {title, url: .private_url}'
```

### JSON Output Features

- **Pretty-printed**: 2-space indentation for readability
- **Consistent format**: All commands return structured JSON with predictable schemas
- **Error handling**: Errors are written to stderr (plain text), data to stdout (JSON)
- **Non-interactive**: Automatically disables interactive prompts and confirmations
- **Pipe-friendly**: Clean stdout makes it perfect for piping to tools like `jq`, `python -m json.tool`, etc.

### Example JSON Outputs

```bash
# Database list
notion db list --json
{
  "databases": [
    {
      "id": "abc123...",
      "title": "Tasks",
      "url": "https://notion.so/...",
      "created_time": "2024-01-01T00:00:00.000Z",
      "last_edited_time": "2024-01-15T12:30:00.000Z"
    }
  ]
}

# Database entries with metadata
notion db show "Tasks" --limit 5 --json
{
  "database": {
    "id": "abc123...",
    "title": "Tasks",
    "url": "https://notion.so/..."
  },
  "entries": [
    {
      "id": "entry123...",
      "url": "https://notion.so/...",
      "properties": {
        "Name": "Review quarterly reports",
        "Status": "In Progress",
        "Priority": "High"
      }
    }
  ],
  "metadata": {
    "total_count": 42,
    "shown_count": 5,
    "limit": 5,
    "filter": null,
    "columns": ["Name", "Status", "Priority"]
  }
}

# Create entry
notion db create "New task" --json
{
  "success": true,
  "entry_id": "xyz789...",
  "url": "https://notion.so/...",
  "properties": {
    "Name": "New task",
    "Status": "Not Started"
  }
}
```

## Advanced Examples

```bash
# Set defaults to streamline workflow
notion db set-default "Hiring"
notion view set-default "active-candidates"

# Filter and save as view (with prefix matching)
notion db show "Hir" --filter "status not in 'Rejected,Declined'" --save-view "active-candidates"

# Use saved view with prefix matching
notion view show "active"  # Matches "active-candidates"
notion view show  # Uses default view

# Create pages in databases with properties
notion page create --parent-name "Projects" --properties '{"Name": "New Feature", "Status": "Planning"}'

# Create pages with JSON blocks
notion page create --parent-id "db-id" --blocks '[{"object": "block", "type": "paragraph", ...}]'

# Create pages from markdown files in databases
notion page create --file "spec.md" --parent-name "Projects" --properties '{"Status": "Active"}'

# Create pages in pages (subpages)
notion page create --file "notes.md" --parent-name "Parent Page Title"

# Interactive AI creation with improved syntax
notion db create "New ML project for customer segmentation" --database "Projects" --interactive --file requirements.txt

# Copy page links to clipboard
notion page link "Meeting Notes" --copy

# View current defaults
notion db get-default
notion view get-default

# Prefix matching with multiple matches shows selection menu
notion db show "Pro"  # If you have "Projects" and "Proposals", shows menu to choose
```

## Page Management

### Page Creation

The `notion page create` command supports multiple ways to create pages:

### Create pages in databases with properties

```bash
# Get database schema to see available properties
notion db properties --id "database-id"

# Create page with properties only
notion page create \
  --parent-id "database-id" \
  --properties '{"Name": "New Page", "Status": "Active", "Priority": "High"}'

# Or use database name
notion page create \
  --parent-name "Projects" \
  --properties '{"Name": "New Feature", "Status": "Planning"}'
```

### Create pages with custom content

```bash
# From markdown file
notion page create \
  --file "spec.md" \
  --parent-name "Projects" \
  --properties '{"Status": "Active"}'

# With JSON blocks (Notion block format)
notion page create \
  --parent-id "database-id" \
  --properties '{"Name": "Design Doc"}' \
  --blocks '[{"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Overview"}}]}}]'
```

### Create pages within pages (subpages)

```bash
# From markdown file
notion page create --file "notes.md" --parent-name "Meeting Notes"

# With custom blocks
notion page create \
  --parent-id "page-id" \
  --blocks '[{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Content here"}}]}}]'
```

### Key features
- **Flexible content**: Use `--file` for markdown or `--blocks` for JSON blocks
- **Database support**: Use `--properties` to set database properties (get schema via `notion db properties`)
- **Parent types**: Supports both database parents and page parents
- **Automatic detection**: `--parent-id` automatically detects database vs page
- **JSON mode**: All options work with `--json` for scripting

### Page Updates

The `notion page update` command allows you to update existing pages:

```bash
# Update page content from markdown file
notion page update "Meeting Notes" --file "updated-notes.md"

# Update by page ID
notion page update --id "abc123" --file "content.md"

# Update properties only
notion page update "Design Doc" --properties '{"Status": "Published", "Priority": "High"}'

# Update both content and properties
notion page update "Project Plan" \
  --file "plan.md" \
  --properties '{"Status": "Active"}'

# Update with JSON blocks
notion page update --id "page-id" \
  --blocks '[{"object": "block", "type": "paragraph", ...}]'

# Update pages in databases (properties get converted automatically)
notion page update "Task Item" \
  --properties '{"Status": "Done", "Priority": "Low"}'
```

### Key features
- **Complete replacement**: `--file` and `--blocks` completely replace page content
- **Property updates**: Use `--properties` to update page properties
- **Smart title extraction**: If markdown starts with `# Title`, it updates the page title
- **Database-aware**: Automatically handles property conversion for database pages
- **Fuzzy search**: Find pages by partial name match
- **JSON mode**: Full support for `--json` output

## Configuration

The CLI automatically prompts for both model selection and API key when first using AI features. No manual configuration required!

```bash
# Example: First time using AI features
notion db create "Add a new task"
# ↳ Will show model selection menu and prompt for API key
# ↳ Saves configuration for future use

# Optional environment variables
NOTION_TOKEN=ntn_...  # optional, can use 'notion auth setup' instead
NOTION_CLI_LLM_MODEL=gpt-4o  # optional, overrides saved model choice
```

### Supported Models
- **OpenAI**: All OpenAI models (gpt-4.1-mini is default)
- **Anthropic**: All Claude models
- **Google**: All Gemini models
- **Other**: Any model supported by LiteLLM


## Help

```bash
notion --help           # General help
notion db --help        # Database commands
notion completion install bash  # Enable tab completion
```
