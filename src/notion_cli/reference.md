# Notion CLI - Command Reference for LLMs

## Auth Commands
- `notion auth setup --token <TOKEN>` - Setup integration token
- `notion auth test` - Test API connection; `--json` for machine output

## Database Commands

### List & Show
- `notion db list` - List all databases; `--json` for output
- `notion db show [NAME]` - Show entries; opts: `--limit N`, `--columns COL1,COL2`, `--filter EXPR`, `--json`
- Examples:
  ```
  notion db show "Tasks" --limit 5 --columns "Name,Status"
  notion db show --filter "Priority=High AND Status!=Done"
  ```

### Create & Edit
- `notion db create "PROMPT"` - Create entry via AI; opts: `--database NAME`, `--file PATH`, `--interactive`, `--json`
  ```
  notion db create "Add task due Friday"
  notion db create "New item" --database "Tasks" --file spec.txt
  ```
- `notion db edit "PROMPT"` - Edit entries via AI; opts: `--database NAME`
  ```
  notion db edit "Mark all completed tasks as done"
  ```

### Defaults
- `notion db set-default "NAME"` - Set default database
- `notion db get-default` - Get default database; `--json` for output

### Links
- `notion db link "NAME"` - Get database URL; opts: `--copy`, `--json`
- `notion db entry-link "DB" "QUERY"` - Get entry URL; opts: `--copy`, `--json`
  ```
  notion db entry-link "Tasks" "meeting"
  ```

### Schema
- `notion db properties --id ID` - Show database schema

## View Commands (Saved Filters)
- `notion view list` - List saved views; `--json` for output
- `notion view show [NAME]` - Display view; `--json` for output
- `notion view set-default "NAME"` - Set default view
- `notion view get-default` - Get default view; `--json` for output
- `notion view delete "NAME"` - Delete view
- `notion view update "NAME"` - Update view; opts: `--columns COL1,COL2`
- Save view: `notion db show "DB" --filter "EXPR" --columns "COLS" --save-view "name"`

## Page Commands
- `notion page view "NAME"` - View page; opts: `--id ID`, `--json`. Default output is markdown.
  ```
  notion page view "Project Plan" --json
  ```
- `notion page find "QUERY"` - Search pages; opts: `--exact`, `--limit N`, `--json`
  ```
  notion page find "Meeting" --limit 10
  ```
- `notion page list` - List all pages; `--json` for output
- `notion page create` - Create page; opts: `--file PATH`, `--parent-name NAME`, `--parent-id ID`, `--properties JSON`, `--blocks JSON`
  ```
  notion page create --file "spec.md" --parent-name "Projects"
  ```
- `notion page update "NAME"` - Update page; opts: `--id ID`, `--file PATH`, `--properties JSON`, `--blocks JSON`
  ```
  notion page update "Meeting Notes" --file "notes.md"
  ```
- `notion page link "NAME"` - Get page URL; opts: `--copy`, `--json`

## Notion Block Format (for --blocks parameter)

The `--blocks` parameter in `notion page create` and `notion page update` expects JSON in **Notion API block format**.

### Block Structure
All blocks must follow this structure:
```json
{
  "object": "block",
  "type": "<block_type>",
  "<block_type>": {
    "rich_text": [{"text": {"content": "text content"}}],
    ...additional properties...
  }
}
```

### Common Block Types

**Paragraph:**
```json
{
  "object": "block",
  "type": "paragraph",
  "paragraph": {
    "rich_text": [{"text": {"content": "This is a paragraph."}}]
  }
}
```

**Headings (heading_1, heading_2, heading_3):**
```json
{
  "object": "block",
  "type": "heading_2",
  "heading_2": {
    "rich_text": [{"text": {"content": "Section Title"}}]
  }
}
```

**Bulleted List Item:**
```json
{
  "object": "block",
  "type": "bulleted_list_item",
  "bulleted_list_item": {
    "rich_text": [{"text": {"content": "List item text"}}]
  }
}
```

**Numbered List Item:**
```json
{
  "object": "block",
  "type": "numbered_list_item",
  "numbered_list_item": {
    "rich_text": [{"text": {"content": "Numbered item"}}]
  }
}
```

**To-Do / Checkbox:**
```json
{
  "object": "block",
  "type": "to_do",
  "to_do": {
    "rich_text": [{"text": {"content": "Task description"}}],
    "checked": false
  }
}
```

**Code Block:**
```json
{
  "object": "block",
  "type": "code",
  "code": {
    "rich_text": [{"text": {"content": "console.log('hello');"}}],
    "language": "javascript"
  }
}
```

**Quote:**
```json
{
  "object": "block",
  "type": "quote",
  "quote": {
    "rich_text": [{"text": {"content": "Quoted text"}}]
  }
}
```

**Callout:**
```json
{
  "object": "block",
  "type": "callout",
  "callout": {
    "rich_text": [{"text": {"content": "Important note"}}],
    "icon": {"emoji": "💡"}
  }
}
```

**Divider:**
```json
{
  "object": "block",
  "type": "divider",
  "divider": {}
}
```

### Complete Example
```bash
notion page create --parent-name "Projects" \
  --properties '{"Name": {"title": [{"text": {"content": "Project Plan"}}]}}' \
  --blocks '[
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{"text": {"content": "Goals"}}]
      }
    },
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{"text": {"content": "Complete the project by end of month."}}]
      }
    },
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{"text": {"content": "Tasks"}}]
      }
    },
    {
      "object": "block",
      "type": "to_do",
      "to_do": {
        "rich_text": [{"text": {"content": "Setup environment"}}],
        "checked": false
      }
    },
    {
      "object": "block",
      "type": "to_do",
      "to_do": {
        "rich_text": [{"text": {"content": "Write code"}}],
        "checked": false
      }
    },
    {
      "object": "block",
      "type": "to_do",
      "to_do": {
        "rich_text": [{"text": {"content": "Deploy"}}],
        "checked": true
      }
    }
  ]'
```

### Updating Page Blocks
When updating with `notion page update --blocks`, all existing blocks are **replaced**:
```bash
notion page update "Page Name" --blocks '[
  {
    "object": "block",
    "type": "paragraph",
    "paragraph": {
      "rich_text": [{"text": {"content": "New content replaces old."}}]
    }
  }
]'
```

### Rich Text Formatting
For styled text, use annotations:
```json
{
  "object": "block",
  "type": "paragraph",
  "paragraph": {
    "rich_text": [
      {"text": {"content": "Normal text "}},
      {
        "text": {"content": "bold text"},
        "annotations": {"bold": true}
      },
      {"text": {"content": " and "}},
      {
        "text": {"content": "italic text"},
        "annotations": {"italic": true}
      }
    ]
  }
}
```

## Other Commands
- `notion completion install SHELL` - Install shell completion (bash/zsh)
- `notion completion show SHELL` - View completion script
- `notion completion uninstall SHELL` - Remove completion
- `notion version` - Show CLI version; `--json` for output
- `notion --help` / `notion COMMAND --help` - Show help

## Filter Syntax
```
Status=Done
Priority=High AND Status!=Archived
Priority=High AND (Status=In Progress OR Status=Blocked)
Status not in 'Rejected,Declined'
```

## Global Options
- `--json` - Machine-readable JSON output (all commands)
- `--model MODEL` - Override LLM model (AI commands)
- `--interactive` - Revise AI output before confirming (create/edit)

## Environment Variables
- `NOTION_TOKEN` - Override config token
- `NOTION_CLI_LLM_MODEL` - Override model selection (default: gpt-4-mini)
- Supported models: GPT-4, Claude, Gemini, any LiteLLM model

## Prefix Matching
DB/view names match by prefix if unique:
```
notion db show "Task"  # Matches "Tasks" if unique
notion view show "act"  # Matches "active-candidates" if unique
```

## JSON Output & Scripting
```bash
# Extract database IDs
notion db list --json | jq '.databases[].id'

# Create and capture ID
ENTRY_ID=$(notion db create "Task" --json | jq -r '.entry_id')

# Filter entries by status
notion db show "Tasks" --json | jq '.entries[] | select(.properties.Status == "Done")'

# Export to CSV
notion db show "Tasks" --json | jq -r '.entries[] | [.properties.Name, .properties.Status] | @csv'
```

## Common Workflows
- **Setup**: `notion auth setup --token <TOKEN>` → `notion db list`
- **Quick view**: `notion db show` (uses default DB)
- **AI create**: `notion db create "description"` → approve in interactive mode
- **Batch ops**: `notion db list --json | jq -r '.databases[].title' | while read db; do notion db show "$db" --limit 5; done`
- **Team views**: Save filter with `--save-view`, share name with team for `notion view show "name"`
