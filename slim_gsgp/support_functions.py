import ast
import json
import inspect
from radon.complexity import cc_visit
import ast
import re
import csv
import os 
def load_data(file_name):
    with open(file_name, "r") as f:
        return json.load(f)
    
    
def write_list_to_csv(data_list, file_name):
    with open(file_name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data_list)

def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)  # `exist_ok=True` prevents errors if the folder already exists
        print(f"Folder '{folder_path}' created successfully.")
    except Exception as e:
        print(f"Error: {e}")

def normalize_tree(tree):
    """Parses and normalizes two code snippets, ignoring variable names."""
    class NameNormalizer(ast.NodeTransformer):
        def visit_Name(self, node):
            return ast.copy_location(ast.Name(id="_var_", ctx=node.ctx), node)

    normalize = lambda code: ast.dump(NameNormalizer().visit(ast.parse(code)), annotate_fields=False)
    return normalize(tree)

#function to calculate SLOC of a function
def count_sloc(source_code):
    """Calculate SLOC (Source Lines of Code) for a function."""
    try:
        source_lines = source_code.split("\n")
        sloc = sum(1 for line in source_lines if line.strip() and not line.strip().startswith("#"))
        return sloc
    except TypeError:
        print("The function might be built-in or not accessible.")
        return 0
    

#count nodes in an ast tree
def count_nodes(node):
    """Recursively count the number of AST nodes."""
    return 1 + sum(count_nodes(child) for child in ast.iter_child_nodes(node))


#calculate max depth of an ast tree
def max_depth(node):
    """Recursively compute the depth of the AST tree."""
    if not list(ast.iter_child_nodes(node)):  # If no children, depth is 1 (leaf node)
        return 1
    return 1 + max(max_depth(child) for child in ast.iter_child_nodes(node))
    
