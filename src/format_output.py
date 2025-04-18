from typing import List, Dict, Union
from rich.console import Console
from rich.syntax import Syntax

console = Console()

def print_code_snippet(code: str, language: str = "python"):
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    console.print(syntax)

def get_snippet(file_path: str, line_number: int, parsed_files: list, window: int = 2) -> str:
    """
    Extracts a code snippet centered around a line number from parsed_files.
    """
    for file in parsed_files:
        if file.path == file_path:
            lines = file.content.splitlines()
            start = max(0, line_number - 1 - window)
            end = min(len(lines), line_number + window)
            snippet = "\n".join(lines[start:end])
            return snippet
    return ""

def format_definition(symbol_info, parsed_files):
    if not symbol_info:
        return "Symbol not found."

    output = f"**Definition**\n"
    output += f"• Type: `{symbol_info.type}`\n"
    output += f"• File: `{symbol_info.file}`\n"
    output += f"• Line: `{symbol_info.line}`\n"

    if symbol_info.docstring:
        output += f"• Docstring: _{symbol_info.docstring}_\n"

    snippet = get_snippet(symbol_info.file, symbol_info.line, parsed_files)
    return (output, snippet)

def format_usages(usages, parsed_files):
    if not usages:
        return "No usages found."

    lines = ["**Usage Locations:**"]
    for use in usages:
        lines.append(f"• `{use['file']}` line {use['line']} (score: {use.get('score', 1)})")
        snippet = get_snippet(use["file"], use["line"], parsed_files)

    return ("\n".join(lines), snippet)

def format_summary(summary: Union[str, Dict[str, Union[str, int, List[str]]]]) -> str:
    if isinstance(summary, str):
        return summary  # error or plain message

    lines = [f"**File Summary: `{summary['file']}`**"]
    lines.append(f"• Total lines: {summary['lines']}")
    if summary.get("functions"):
        lines.append(f"• Functions: {', '.join(summary['functions'])}")
    if summary.get("classes"):
        lines.append(f"• Classes: {', '.join(summary['classes'])}")
    return "\n".join(lines)

def format_generic_results(results: List[Dict[str, Union[str, int]]]) -> str:
    if not results:
        return "🔍 No relevant matches found."

    lines = ["🔎 **Search Results:**"]
    for res in results:
        lines.append(f"• `{res['file']}` line {res['line']}")
    return "\n".join(lines)

# Optional unified formatter based on query type
def format_response(query_type: str, result: Union[str, dict, list], parsed_files=None):
    if query_type == "definition":
        return format_definition(result, parsed_files)
    elif query_type == "usage":
        return format_usages(result, parsed_files)
    elif query_type == "summary":
        return format_summary(result)
    elif query_type == "generic_search":
        return format_generic_results(result)
    elif query_type == "library_usage":
        return format_generic_results(result)
    else:
        return str(result)
