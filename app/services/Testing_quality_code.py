import ast
import os


def analyze_code(folder_path):
    all_file = { }
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                all_file[file]=(analyze_file(full_path))
    return all_file
def analyze_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    tree = ast.parse(source)
    file_dict = {}
    file_dict["len"] = sum(isinstance(node,ast.stmt) for node in ast.walk(tree))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_length = get_function_length(node)
            list_undefined = undefined_variable_analyzer(node)
            is_docstring = has_docstring_manual(node)
            file_dict[node.name] = {
           'func_length': func_length,
           'list_undefined' : list_undefined,
            'is_docstring' : is_docstring
            }

    return file_dict

def get_function_length(func_node: ast.FunctionDef) -> int:
    start_line = func_node.lineno
    end_line = max(
        (child.lineno for child in ast.walk(func_node) if hasattr(child, 'lineno')),
        default=start_line
    )
    return end_line - start_line + 1


def undefined_variable_analyzer(func_node: ast.FunctionDef):
    defined_vars = set()
    used_vars = set()
    for node in ast.walk(func_node):
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                defined_vars.add(node.id)
            elif isinstance(node.ctx, ast.Load):
                used_vars.add(node.id)

    unused_vars = defined_vars - used_vars
    return list(unused_vars)


def has_docstring_manual(func_node: ast.FunctionDef):
    return ast.get_docstring(func_node) is not None






