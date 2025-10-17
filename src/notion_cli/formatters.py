"""Output formatting utilities for both Rich and JSON output modes."""

import json
import sys
from typing import Any

import typer
from rich.console import Console
from rich.table import Table


class OutputFormatter:
    """Centralized output formatting for both Rich tables and JSON."""

    @staticmethod
    def _extract_plain_text(rich_text_array: list[dict[str, Any]]) -> str:
        """Extract plain text from Notion's rich text array format."""
        if not rich_text_array:
            return ""
        if isinstance(rich_text_array, list):
            return "".join(item.get("plain_text", "") for item in rich_text_array)
        return str(rich_text_array)

    @staticmethod
    def _clean_notion_object(obj: dict[str, Any]) -> dict[str, Any]:
        """Remove internal/unnecessary Notion API fields."""
        cleaned = {}
        # Fields to exclude from JSON output
        exclude_fields = {"object", "type", "parent", "archived", "cover", "icon"}

        for key, value in obj.items():
            if key in exclude_fields:
                continue

            # Clean nested structures
            if isinstance(value, dict):
                if "plain_text" in value:
                    cleaned[key] = value["plain_text"]
                elif key == "properties":
                    # Properties need special handling
                    cleaned[key] = OutputFormatter._extract_simple_properties(value)
                else:
                    cleaned[key] = OutputFormatter._clean_notion_object(value)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                if "plain_text" in value[0]:
                    # Rich text array
                    cleaned[key] = OutputFormatter._extract_plain_text(value)
                else:
                    cleaned[key] = [
                        OutputFormatter._clean_notion_object(item)
                        if isinstance(item, dict)
                        else item
                        for item in value
                    ]
            else:
                cleaned[key] = value

        return cleaned

    @staticmethod
    def _extract_simple_properties(properties: dict[str, Any]) -> dict[str, Any]:
        """Convert Notion property format to simple key-value pairs."""
        simple_props = {}

        for prop_name, prop_data in properties.items():
            prop_type = prop_data.get("type", "")

            # Extract value based on property type
            if prop_type == "title" and "title" in prop_data:
                simple_props[prop_name] = OutputFormatter._extract_plain_text(
                    prop_data["title"]
                )
            elif prop_type == "rich_text" and "rich_text" in prop_data:
                simple_props[prop_name] = OutputFormatter._extract_plain_text(
                    prop_data["rich_text"]
                )
            elif prop_type == "number" and "number" in prop_data:
                simple_props[prop_name] = prop_data["number"]
            elif prop_type == "select" and "select" in prop_data:
                select_value = prop_data["select"]
                simple_props[prop_name] = select_value.get("name") if select_value else None
            elif prop_type == "multi_select" and "multi_select" in prop_data:
                simple_props[prop_name] = [
                    item.get("name") for item in prop_data["multi_select"]
                ]
            elif prop_type == "date" and "date" in prop_data:
                date_value = prop_data["date"]
                if date_value:
                    simple_props[prop_name] = {
                        "start": date_value.get("start"),
                        "end": date_value.get("end"),
                    }
                else:
                    simple_props[prop_name] = None
            elif prop_type == "checkbox" and "checkbox" in prop_data:
                simple_props[prop_name] = prop_data["checkbox"]
            elif prop_type == "url" and "url" in prop_data:
                simple_props[prop_name] = prop_data["url"]
            elif prop_type == "email" and "email" in prop_data:
                simple_props[prop_name] = prop_data["email"]
            elif prop_type == "phone_number" and "phone_number" in prop_data:
                simple_props[prop_name] = prop_data["phone_number"]
            elif prop_type == "files" and "files" in prop_data:
                simple_props[prop_name] = [
                    {"name": f.get("name"), "url": f.get("url", f.get("file", {}).get("url"))}
                    for f in prop_data["files"]
                ]
            elif prop_type == "relation" and "relation" in prop_data:
                simple_props[prop_name] = [rel.get("id") for rel in prop_data["relation"]]
            elif prop_type == "people" and "people" in prop_data:
                simple_props[prop_name] = [
                    person.get("name", person.get("id")) for person in prop_data["people"]
                ]
            else:
                # For unknown types, include raw data
                simple_props[prop_name] = prop_data.get(prop_type)

        return simple_props

    @staticmethod
    def _output_json(data: Any, indent: int = 2) -> None:
        """Print JSON to stdout with specified indentation."""
        json.dump(data, sys.stdout, indent=indent, ensure_ascii=False)
        sys.stdout.write("\n")
        sys.stdout.flush()

    @staticmethod
    def format_databases(databases: list[dict[str, Any]], as_json: bool = False) -> Any:
        """Format databases for output."""
        if as_json:
            output = []
            for db in databases:
                # Extract title
                title = "Untitled"
                if "title" in db and db["title"]:
                    if isinstance(db["title"], list) and db["title"]:
                        title = db["title"][0].get("plain_text", "Untitled")
                    elif isinstance(db["title"], str):
                        title = db["title"]

                output.append(
                    {
                        "id": db.get("id", ""),
                        "title": title,
                        "url": db.get("url", ""),
                        "created_time": db.get("created_time"),
                        "last_edited_time": db.get("last_edited_time"),
                    }
                )
            return {"databases": output}
        else:
            # Return Rich Table
            table = Table(title="Notion Databases")
            table.add_column("Name", style="cyan")
            table.add_column("ID", style="magenta")
            table.add_column("URL", style="blue")

            for db in databases:
                title = "Untitled"
                if "title" in db and db["title"]:
                    if isinstance(db["title"], list) and db["title"]:
                        title = db["title"][0].get("plain_text", "Untitled")
                    elif isinstance(db["title"], str):
                        title = db["title"]

                db_id = db.get("id", "")
                db_url = db.get("url", "")
                table.add_row(title, db_id, db_url)

            return table

    @staticmethod
    def format_database_entries(
        entries: list[dict[str, Any]],
        properties: dict[str, Any],
        displayed_props: list[str],
        as_json: bool = False,
    ) -> Any:
        """Format database entries for output."""
        if as_json:
            output = []
            for entry in entries:
                entry_data = {
                    "id": entry.get("id", ""),
                    "url": entry.get("url", ""),
                    "properties": {},
                }

                entry_properties = entry.get("properties", {})
                for prop_name in displayed_props:
                    if prop_name in entry_properties:
                        prop_data = entry_properties[prop_name]
                        # Use the simple property extraction
                        simplified = OutputFormatter._extract_simple_properties(
                            {prop_name: prop_data}
                        )
                        entry_data["properties"][prop_name] = simplified.get(prop_name)

                output.append(entry_data)

            return output
        else:
            return None  # Rich table is handled separately in main.py

    @staticmethod
    def format_pages(pages: list[dict[str, Any]], as_json: bool = False) -> Any:
        """Format pages for output."""
        if as_json:
            output = []
            for page in pages:
                title = page.get("_title", "Untitled")
                output.append(
                    {
                        "id": page.get("id", ""),
                        "title": title,
                        "url": page.get("url", ""),
                        "created_time": page.get("created_time"),
                        "last_edited_time": page.get("last_edited_time"),
                    }
                )
            return {"pages": output}
        else:
            # Return Rich Table
            table = Table(title="Notion Pages")
            table.add_column("Name", style="cyan")
            table.add_column("ID", style="magenta")
            table.add_column("URL", style="blue")

            for page in pages:
                title = page.get("_title", "Untitled")
                page_id = page.get("id", "")
                page_url = page.get("url", "")
                table.add_row(title, page_id, page_url)

            return table

    @staticmethod
    def format_views(views: list[Any], as_json: bool = False) -> Any:
        """Format saved views for output."""
        if as_json:
            output = []
            for view in views:
                output.append(
                    {
                        "name": view.name,
                        "database_name": view.database_name,
                        "columns": view.columns if view.columns else None,
                        "filter": view.filter_expr if view.filter_expr else None,
                        "limit": view.limit if view.limit else None,
                        "description": view.description if view.description else None,
                    }
                )
            return {"views": output}
        else:
            # Return Rich Table
            table = Table(title="Saved Views")
            table.add_column("Name", style="cyan")
            table.add_column("Database", style="green")
            table.add_column("Columns", style="blue")
            table.add_column("Filter", style="magenta")
            table.add_column("Limit", style="white")

            for view in views:
                columns_str = ", ".join(view.columns) if view.columns else "All"
                filter_str = view.filter_expr if view.filter_expr else "None"
                limit_str = str(view.limit) if view.limit else "All"

                table.add_row(
                    view.name,
                    view.database_name,
                    columns_str,
                    filter_str,
                    limit_str,
                )

            return table

    @staticmethod
    def format_success(message: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """Format a success response for JSON output."""
        result: dict[str, Any] = {"success": True}
        if data:
            result.update(data)
        return result

    @staticmethod
    def output_json(data: Any) -> None:
        """Output data as pretty-printed JSON to stdout."""
        OutputFormatter._output_json(data)


def handle_error(
    message: str,
    json_mode: bool = False,
    exit_code: int = 1,
    console: Console | None = None,
) -> None:
    """Handle errors consistently across JSON and Rich output modes."""
    if json_mode:
        # Write plain text error to stderr
        sys.stderr.write(f"Error: {message}\n")
        sys.stderr.flush()
    else:
        # Use Rich console for formatted error
        if console is None:
            console = Console()
        console.print(f"❌ {message}", style="red")

    raise typer.Exit(exit_code)


def output_result(data: Any, json_mode: bool = False, console: Console | None = None) -> None:
    """Output result in either JSON or Rich format."""
    if json_mode:
        OutputFormatter.output_json(data)
    else:
        if console is None:
            console = Console()
        if isinstance(data, Table):
            console.print(data)
        elif isinstance(data, dict):
            # For dict data in non-JSON mode, format nicely
            for key, value in data.items():
                console.print(f"{key}: {value}")
        else:
            console.print(data)
