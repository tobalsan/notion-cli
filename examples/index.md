# Notion CLI - Comprehensive Examples

This document contains exhaustive command references, arguments, options, and usage examples for all `notion-cli` functionality.

## Table of Contents

1. [Authentication](#authentication)
2. [Database Operations](#database-operations)
3. [Saved Views](#saved-views)
4. [Page Management](#page-management)
5. [JSON Output & Scripting](#json-output--scripting)
6. [Advanced Examples](#advanced-examples)

---

## Authentication

### Setup

```bash
# Create a Notion Integration at https://www.notion.so/my-integrations
# Copy the integration token and run:
notion auth setup --token <your-integration-token>
```

You can also simply `cp .env.example .env` and set the `NOTION_TOKEN` variable.

### Test Connection

```bash
notion auth test
notion auth test --json
```

---

## Database Operations

### List Databases

**Usage:**
```bash
notion db list
notion db list --json
```

**Output:** List of all accessible Notion databases with IDs, URLs, and timestamps.

### Set Default Database

```bash
notion db set-default "Tasks"
notion db get-default
```

**Use case:** Avoid typing database names repeatedly in subsequent commands.

### Show Database Entries

**Basic:**
```bash
notion db show "Tasks"
notion db show  # Uses default database
```

**With Options:**
```bash
# Limit results
notion db show "Tasks" --limit 10

# Custom columns
notion db show "Tasks" --columns "Name,Status,Priority"

# Filter entries
notion db show "Tasks" --filter "Status=Done"
notion db show "Tasks" --filter "Priority=High AND Status!=Archived"

# Combine options
notion db show "Tasks" --limit 5 --columns "Name,Due Date" --filter "Status=In Progress"

# JSON output
notion db show "Tasks" --json
notion db show "Tasks" --filter "Status=Done" --json | jq '.entries[] | {id, name: .properties.Name}'
```

**Filter Syntax:**
```bash
# Simple equality
--filter "Status=Done"

# Multiple conditions with AND
--filter "Status=Done AND Priority=High"

# NOT operator
--filter "Status!=Archived"

# NOT in list
--filter "Status not in 'Rejected,Declined'"

# Complex queries
--filter "Priority=High AND (Status=In Progress OR Status=Blocked)"
```

### Create Entries with AI

**Natural language creation:**
```bash
notion db create "Add high priority task to review quarterly reports due Friday"
notion db create "Add high priority task to review quarterly reports" --database "Tasks"
```

**With file attachment:**
```bash
notion db create "New project with attached spec" --file requirements.txt
```

**Interactive mode (revise AI output):**
```bash
notion db create "New task" --interactive
```

**JSON output:**
```bash
ENTRY_ID=$(notion db create "New task" --json | jq -r '.entry_id')
```

### Edit Entries with AI

```bash
notion db edit "Mark all completed tasks as archived"
notion db edit "Mark all tasks assigned to John as high priority" --database "Tasks"
```

The AI interprets the prompt to generate:
- Filter expression to find matching entries
- Property updates to apply

### Database Links

```bash
notion db link "Tasks"
notion db link "Tasks" --copy  # Copy to clipboard
notion db link "Tasks" --json  # Get URL programmatically
```

### Entry Links

```bash
notion db entry-link "Tasks" "meeting"
notion db entry-link "Tasks" "meeting" --copy
notion db entry-link "Tasks" "meeting" --json
```

### Database Properties Schema

```bash
notion db properties --id "database-id"
```

---

## Saved Views

Save filtered/columned views for quick access.

### List Views

```bash
notion view list
notion view list --json
```

### Create View

```bash
# Create by saving current filter/columns
notion db show "Tasks" --filter "Status=Done" --columns "Name,Priority" --save-view "completed"

# View is saved and can be referenced as "completed"
```

### Show View

```bash
notion view show "completed"
notion view show  # Uses default view if set
```

### Set Default View

```bash
notion view set-default "active-candidates"
notion view get-default
```

### Manage Views

```bash
notion view delete "completed"
notion view update "completed" --columns "Name,Status,Due Date"
```

### View Operations with Prefix Matching

```bash
# Prefix matching works for views too
notion view show "act"  # Matches "active-candidates" if unique

# If multiple matches, CLI shows selection menu
notion view show "pro"  # Shows menu if "projects" and "proposals" exist
```

---

## Page Management

### Find Pages

```bash
notion page find "Meeting Notes"
notion page list  # All pages
notion page find "Meeting" --exact  # Exact match
notion page find "Project" --limit 10
notion page find "Design" --json
```

### Create Pages

**From markdown file:**
```bash
notion page create --file "spec.md" --parent-name "Projects"
```

**With properties (in databases):**
```bash
notion page create \
  --parent-name "Projects" \
  --properties '{"Name": "New Feature", "Status": "Planning"}'
```

**With custom blocks:**
```bash
notion page create \
  --parent-id "database-id" \
  --properties '{"Name": "Design Doc"}' \
  --blocks '[{"object": "block", "type": "heading_2", ...}]'
```

**Subpages (within pages):**
```bash
notion page create --file "notes.md" --parent-name "Meeting Notes"
```

**Using parent ID:**
```bash
notion page create --file "content.md" --parent-id "abc123"
```

### Update Pages

```bash
# Update content from markdown
notion page update "Meeting Notes" --file "updated-notes.md"

# Update by ID
notion page update --id "page-id" --file "content.md"

# Update properties only
notion page update "Design Doc" --properties '{"Status": "Published", "Priority": "High"}'

# Update both content and properties
notion page update "Project Plan" \
  --file "plan.md" \
  --properties '{"Status": "Active"}'

# Update with blocks
notion page update --id "page-id" \
  --blocks '[{"object": "block", "type": "paragraph", ...}]'
```

### Page Links

```bash
notion page link "Meeting Notes"
notion page link "Meeting Notes" --copy  # Copy to clipboard
notion page find "Meeting" --json | jq '.pages[] | {title, url: .private_url}'
```

---

## JSON Output & Scripting

All commands support `--json` for machine-readable output. Errors go to stderr, data to stdout.

### Basic JSON Queries

```bash
# List databases as JSON
notion db list --json

# Get default database
notion db get-default --json

# List views
notion view list --json

# List pages
notion page list --json

# Check version
notion version --json
```

### Filtering with jq

```bash
# Get all database titles
notion db list --json | jq '.databases[].title'

# Find specific database
notion db list --json | jq '.databases[] | select(.title == "Tasks")'

# Extract fields
notion db list --json | jq '.databases[] | {title, id, url}'

# Count databases
notion db list --json | jq '.databases | length'
```

### Database Entry Queries

```bash
# Show entries with metadata
notion db show "Tasks" --json | jq '{total: .metadata.total_count, entries: .entries | length}'

# Filter and extract properties
notion db show "Tasks" --filter "Status=Done" --json | jq '.entries[] | {id, name: .properties.Name}'

# Get database link programmatically
notion db link "Tasks" --json | jq -r '.url'
```

### Creating Entries Programmatically

```bash
# Capture entry ID
ENTRY_ID=$(notion db create "New task: review reports" --json | jq -r '.entry_id')
echo "Created entry: $ENTRY_ID"

# Get entry URL
URL=$(notion db create "New task" --json | jq -r '.url')
```

### Page Queries

```bash
# Find pages and extract URLs
notion page find "Meeting" --json | jq '.pages[] | {title, url: .private_url}'

# Get pages with match scores
notion page find "Project" --json | jq '.pages[] | {title, match_score, url: .private_url}'
```

### Batch Operations

```bash
# Process multiple databases
notion db list --json | jq -r '.databases[].title' | while read db; do
  echo "Processing: $db"
  notion db show "$db" --limit 5 --json > "${db// /_}.json"
done

# Create multiple entries from file
cat tasks.txt | while read task; do
  notion db create "$task" --json | jq -r '.entry_id'
done

# Export database to JSON
notion db show "Tasks" --json > tasks_export.json
```

### Advanced jq Processing

```bash
# Group entries by status
notion db show "Tasks" --json | \
  jq '.entries | group_by(.properties.Status) | \
      map({status: .[0].properties.Status, count: length})'

# Export to CSV
notion db show "Tasks" --json | \
  jq -r '.entries[] | [.properties.Name, .properties.Status, .url] | @csv' > tasks.csv

# Filter and sort
notion db show "Tasks" --json | \
  jq '.entries | sort_by(.properties.Priority) | .[0:5]'
```

### Integration Examples

```bash
# Check if database exists
DB_EXISTS=$(notion db list --json | jq -r '.databases[] | select(.title == "Tasks") | .id')
if [ -n "$DB_EXISTS" ]; then
  echo "Database exists with ID: $DB_EXISTS"
else
  echo "Database not found"
fi

# Get entry count
ENTRY_COUNT=$(notion db show "Tasks" --json | jq -r '.metadata.total_count')
echo "Total entries: $ENTRY_COUNT"

# Send to webhook
notion db list --json | \
  curl -X POST https://webhook.site/your-webhook \
       -H "Content-Type: application/json" \
       -d @-

# Parse with Python
notion db list --json | python3 -c "
import sys, json
data = json.load(sys.stdin)
for db in data['databases']:
    print(f\"{db['title']}: {db['url']}\")
"

# Pretty print
notion db show "Tasks" --json | python3 -m json.tool | less

# Error handling
notion db show "NonexistentDB" --json 2> errors.log 1> output.json
if [ $? -ne 0 ]; then
  echo "Command failed. Check errors.log"
  cat errors.log
fi

# Check authentication
if notion auth test --json | jq -e '.authenticated' > /dev/null; then
  echo "✅ Authenticated"
else
  echo "❌ Not authenticated"
fi
```

---

## Advanced Examples

### Prefix Matching

Database and view names support prefix matching with automatic resolution:

```bash
# Exact match
notion db show "Tasks"

# Prefix match (if unique)
notion db show "Task"
notion db show "Pro"  # Matches "Projects" if unique

# Multiple matches show selection menu
notion db show "Pro"  # Shows menu if both "Projects" and "Proposals" exist
```

### Configuration

The CLI automatically prompts for model selection and API key on first AI use.

**Environment variables:**
```bash
NOTION_TOKEN=ntn_...  # Optional, overrides config file
NOTION_CLI_LLM_MODEL=gpt-4o  # Optional, overrides saved choice
```

**Supported models:**
- OpenAI: All models (default: gpt-4-mini)
- Anthropic: All Claude models
- Google: All Gemini models
- Other: Any LiteLLM-supported model

### Shell Completions

```bash
notion completion install bash
notion completion install zsh
notion completion show bash  # View completion script
notion completion uninstall bash
```

### Complex Workflows

**Create task with file and interactive refinement:**
```bash
notion db create "Project kickoff with attached brief" \
  --database "Projects" \
  --file brief.pdf \
  --interactive
```

**Filter entries with complex logic:**
```bash
notion db show "Tasks" \
  --filter "Priority=High AND (Status!=Done AND Status!=Archived)" \
  --columns "Name,Status,Priority,Due Date" \
  --limit 20
```

**Save view for team workflow:**
```bash
# Team lead creates view
notion db show "Hiring" \
  --filter "Status not in 'Rejected,Declined'" \
  --columns "Name,Status,Round,Interview Date" \
  --save-view "active-candidates"

# Team members use it
notion view show "active-candidates"
```

**Automated entry creation:**
```bash
# Read from CSV and create entries
awk -F, 'NR>1 {print $1}' tasks.csv | while read task; do
  notion db create "$task" --database "Tasks"
done
```

### JSON Output Features

- Pretty-printed with 2-space indentation
- Consistent schema across all commands
- Errors to stderr (plain text), data to stdout (JSON)
- Non-interactive (disables prompts)
- Pipe-friendly for tool integration

### Help

```bash
notion --help
notion db --help
notion page --help
notion auth --help
```

---

## Command Reference

| Command | Purpose |
|---------|---------|
| `notion auth setup` | Authenticate with Notion API token |
| `notion auth test` | Test API connection |
| `notion db list` | List all databases |
| `notion db show` | Display database entries |
| `notion db create` | Create entries with AI |
| `notion db edit` | Edit entries with AI |
| `notion db link` | Get database URL |
| `notion db entry-link` | Get entry URL |
| `notion db set-default` | Set default database |
| `notion db get-default` | Get default database |
| `notion db properties` | Show database schema |
| `notion view list` | List saved views |
| `notion view show` | Display saved view |
| `notion view set-default` | Set default view |
| `notion view get-default` | Get default view |
| `notion view delete` | Delete saved view |
| `notion view update` | Update saved view |
| `notion page create` | Create new page |
| `notion page update` | Update existing page |
| `notion page find` | Search pages |
| `notion page list` | List all pages |
| `notion page link` | Get page URL |
| `notion completion` | Shell completion management |
| `notion version` | Show CLI version |

