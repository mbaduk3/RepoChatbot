import os
import re
import ast
from collections import defaultdict
from models.FileData import FileData
from models.FuncData import FuncData
from models.ClassData import ClassData
from models.SymbolData import SymbolData 
from typing import List

STOPWORDS = {
    "def", "class", "if", "else", "elif", "return", "in", "for", "while",
    "import", "from", "as", "with", "pass", "print", "and", "or", "not"
}


def scan_repo(root_dir, ext):
    repo_data = scan_repo_to_filedata(root_dir, ext)
    symbol_table = build_symbol_table(repo_data)
    index_inv = build_inverted_index(repo_data)
    return repo_data, symbol_table, index_inv


def scan_repo_to_filedata(root_dir, ext) -> List[FileData]:
    files:List[FileData] = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(ext):
                full_path = os.path.join(dirpath, filename)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                rel_path = os.path.relpath(full_path, root_dir)
                module_path = rel_path.replace(os.sep, ".").replace(ext, "")
                functions, classes = extract_symbols(content)
                file_data = FileData(
                    rel_path,
                    filename,
                    module_path,
                    content,
                    functions,
                    classes)
                files.append(file_data)
    return files


def extract_symbols(code: str):
    functions:List[FuncData] = []
    classes:List[ClassData] = []
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"Syntax error while parsing: {e}")
        return functions, classes
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            fun = FuncData(
                node.name,
                node.lineno,
                ast.get_docstring(node),
                [arg.arg for arg in node.args.args]
            )
            functions.append(fun)
        elif isinstance(node, ast.ClassDef):
            cls = ClassData(
                node.name,
                node.lineno,
                ast.get_docstring(node),
                [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            )
            classes.append(cls) 
    return functions, classes


def tokenize_line(line:str) -> List[str]:
    raw_tokens = re.findall(r'\b\w+\b', line)
    return [token.lower() for token in raw_tokens if token.lower() not in STOPWORDS]


def rank_matches(token, inverted_index, symbol_table):
    matches = inverted_index.get(token.lower(), [])
    ranked = []
    for match in matches:
        score = 1
        file = match["file"]
        line = match["line"]
        sym = symbol_table.get(token)
        if sym and sym["file"] == file and sym["line"] == line:
            score = 3
        elif sym and sym["file"] == file:
            score = 2
        ranked.append({
            "file": file,
            "line": line,
            "score": score
        })
    ranked.sort(key=lambda x: (-x["score"], x["line"]))
    return ranked


def build_inverted_index(parsed_files: List[FileData]):
    index = defaultdict(list)

    for file_data in parsed_files:
        path = file_data.path
        lines = file_data.content.splitlines()

        for lineno, line in enumerate(lines, start=1):
            tokens = tokenize_line(line)
            for token in tokens:
                entry = {"file": path, "line": lineno}
                if entry not in index[token]:
                    index[token].append(entry)

    return index


def build_symbol_table(parsed_files: List[FileData]):
    symbol_table = {}

    for file_data in parsed_files:
        path = file_data.path
        module = file_data.module

        for func in file_data.functions:
            sym = SymbolData(
                path,
                module,
                func.line_num,
                "function",
                func.docstring)
            symbol_table[func.name] = sym

        for cls in file_data.classes:
            sym = SymbolData(
                path,
                module,
                cls.line_num,
                "class",
                cls.docstring)
            symbol_table[cls.name] = sym

    return symbol_table
