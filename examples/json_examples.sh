#!/bin/bash
# JSON Output Examples for notion-cli
# This script demonstrates various ways to use the --json flag with notion-cli commands

echo "=== JSON Output Examples for notion-cli ==="
echo ""

# ==============================================================================
# BASIC USAGE
# ==============================================================================

echo "1. List all databases as JSON"
echo "$ notion db list --json"
notion db list --json
echo ""

echo "2. Get default database as JSON"
echo "$ notion db get-default --json"
notion db get-default --json
echo ""

echo "3. List all saved views as JSON"
echo "$ notion view list --json"
notion view list --json
echo ""

echo "4. List all pages as JSON"
echo "$ notion page list --json"
notion page list --json
echo ""

echo "5. Check version as JSON"
echo "$ notion version --json"
notion version --json
echo ""

# ==============================================================================
# FILTERING WITH JQ
# ==============================================================================

echo ""
echo "=== Filtering and Processing with jq ==="
echo ""

echo "6. Get all database titles"
echo "$ notion db list --json | jq '.databases[].title'"
notion db list --json | jq '.databases[].title'
echo ""

echo "7. Find a specific database by title"
echo "$ notion db list --json | jq '.databases[] | select(.title == \"Tasks\")'"
notion db list --json | jq '.databases[] | select(.title == "Tasks")'
echo ""

echo "8. Extract database IDs and URLs"
echo "$ notion db list --json | jq '.databases[] | {title, id, url}'"
notion db list --json | jq '.databases[] | {title, id, url}'
echo ""

echo "9. Count total number of databases"
echo "$ notion db list --json | jq '.databases | length'"
notion db list --json | jq '.databases | length'
echo ""

# ==============================================================================
# DATABASE OPERATIONS
# ==============================================================================

echo ""
echo "=== Database Operations ==="
echo ""

echo "10. Show database entries with metadata"
echo "$ notion db show \"Tasks\" --json | jq '{total: .metadata.total_count, entries: .entries | length}'"
# Note: Replace "Tasks" with your actual database name
# notion db show "Tasks" --json | jq '{total: .metadata.total_count, entries: .entries | length}'
echo "(Replace 'Tasks' with your database name)"
echo ""

echo "11. Filter database entries and extract specific properties"
echo "$ notion db show \"Tasks\" --filter \"Status=Done\" --json | jq '.entries[] | {id, name: .properties.Name}'"
# notion db show "Tasks" --filter "Status=Done" --json | jq '.entries[] | {id, name: .properties.Name}'
echo "(Replace 'Tasks' with your database name and adjust filter)"
echo ""

echo "12. Get database link programmatically"
echo "$ notion db link \"Tasks\" --json | jq -r '.url'"
# notion db link "Tasks" --json | jq -r '.url'
echo "(Replace 'Tasks' with your database name)"
echo ""

# ==============================================================================
# CREATING ENTRIES
# ==============================================================================

echo ""
echo "=== Creating Entries ==="
echo ""

echo "13. Create entry and capture the entry ID"
echo "$ ENTRY_ID=\$(notion db create \"New task: review reports\" --json | jq -r '.entry_id')"
echo "$ echo \"Created entry: \$ENTRY_ID\""
# ENTRY_ID=$(notion db create "New task: review reports" --json | jq -r '.entry_id')
# echo "Created entry: $ENTRY_ID"
echo "(Uncomment to actually create an entry)"
echo ""

echo "14. Create entry and get the URL"
echo "$ notion db create \"New task\" --json | jq -r '.url'"
# notion db create "New task" --json | jq -r '.url'
echo "(Uncomment to actually create an entry)"
echo ""

# ==============================================================================
# PAGE OPERATIONS
# ==============================================================================

echo ""
echo "=== Page Operations ==="
echo ""

echo "15. Find pages and extract URLs"
echo "$ notion page find \"Meeting\" --json | jq '.pages[] | {title, url: .private_url}'"
# notion page find "Meeting" --json | jq '.pages[] | {title, url: .private_url}'
echo "(Replace 'Meeting' with your search term)"
echo ""

echo "16. Get page link with match scores"
echo "$ notion page find \"Project\" --json | jq '.pages[] | {title, match_score, url: .private_url}'"
# notion page find "Project" --json | jq '.pages[] | {title, match_score, url: .private_url}'
echo "(Replace 'Project' with your search term)"
echo ""

# ==============================================================================
# SCRIPTING AND AUTOMATION
# ==============================================================================

echo ""
echo "=== Scripting and Automation Examples ==="
echo ""

echo "17. Check if a database exists"
cat << 'EOF'
$ DB_EXISTS=$(notion db list --json | jq -r '.databases[] | select(.title == "Tasks") | .id')
$ if [ -n "$DB_EXISTS" ]; then
    echo "Database exists with ID: $DB_EXISTS"
  else
    echo "Database not found"
  fi
EOF
echo ""

echo "18. Get entry count for a database"
cat << 'EOF'
$ ENTRY_COUNT=$(notion db show "Tasks" --json | jq -r '.metadata.total_count')
$ echo "Total entries: $ENTRY_COUNT"
EOF
echo ""

echo "19. Export database to JSON file"
cat << 'EOF'
$ notion db show "Tasks" --json > tasks_export.json
$ echo "Exported to tasks_export.json"
EOF
echo ""

echo "20. Find entries by property value"
cat << 'EOF'
$ notion db show "Tasks" --filter "Priority=High" --json | \
  jq '.entries[] | {name: .properties.Name, status: .properties.Status}'
EOF
echo ""

# ==============================================================================
# ADVANCED JQ EXAMPLES
# ==============================================================================

echo ""
echo "=== Advanced jq Processing ==="
echo ""

echo "21. Group entries by status (requires actual database)"
cat << 'EOF'
$ notion db show "Tasks" --json | \
  jq '.entries | group_by(.properties.Status) |
      map({status: .[0].properties.Status, count: length})'
EOF
echo ""

echo "22. Create a CSV from database entries"
cat << 'EOF'
$ notion db show "Tasks" --json | \
  jq -r '.entries[] | [.properties.Name, .properties.Status, .url] | @csv' > tasks.csv
EOF
echo ""

echo "23. Filter and sort entries"
cat << 'EOF'
$ notion db show "Tasks" --json | \
  jq '.entries | sort_by(.properties.Priority) | .[0:5]'
EOF
echo ""

# ==============================================================================
# ERROR HANDLING
# ==============================================================================

echo ""
echo "=== Error Handling ==="
echo ""

echo "24. Capture errors separately (errors go to stderr)"
cat << 'EOF'
$ notion db show "NonexistentDB" --json 2> errors.log 1> output.json
$ if [ $? -ne 0 ]; then
    echo "Command failed. Check errors.log"
    cat errors.log
  fi
EOF
echo ""

echo "25. Check authentication"
cat << 'EOF'
$ if notion auth test --json | jq -e '.authenticated' > /dev/null; then
    echo "✅ Authenticated"
  else
    echo "❌ Not authenticated"
  fi
EOF
echo ""

# ==============================================================================
# INTEGRATION EXAMPLES
# ==============================================================================

echo ""
echo "=== Integration with Other Tools ==="
echo ""

echo "26. Send database data to a webhook"
cat << 'EOF'
$ notion db list --json | \
  curl -X POST https://webhook.site/your-webhook \
       -H "Content-Type: application/json" \
       -d @-
EOF
echo ""

echo "27. Parse with Python"
cat << 'EOF'
$ notion db list --json | python3 -c "
import sys, json
data = json.load(sys.stdin)
for db in data['databases']:
    print(f\"{db['title']}: {db['url']}\")
"
EOF
echo ""

echo "28. Pretty print with Python"
cat << 'EOF'
$ notion db show "Tasks" --json | python3 -m json.tool | less
EOF
echo ""

# ==============================================================================
# BATCH OPERATIONS
# ==============================================================================

echo ""
echo "=== Batch Operations ==="
echo ""

echo "29. Process multiple databases"
cat << 'EOF'
$ notion db list --json | jq -r '.databases[].title' | while read db; do
    echo "Processing: $db"
    notion db show "$db" --limit 5 --json > "${db// /_}.json"
  done
EOF
echo ""

echo "30. Create multiple entries from a file"
cat << 'EOF'
$ cat tasks.txt | while read task; do
    notion db create "$task" --json | jq -r '.entry_id'
  done
EOF
echo ""

echo ""
echo "=== End of Examples ==="
echo ""
echo "Note: Many examples are commented out or shown as examples."
echo "Uncomment and modify them for your specific use case."
echo ""
echo "For more information, visit: https://github.com/yourusername/notion-cli"
