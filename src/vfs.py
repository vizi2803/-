import os
from typing import Any, Dict, Optional, Tuple

class VFS:
    def __init__(self, root_name = "my_vfs"):
        self.root_name = root_name
        self.root = {}
        self.current_path = []

    def get_node(self, path_parts):
        cursor = self.root
        for part in path_parts:
            if not isinstance(cursor, dict) or part not in cursor:
                return None
            cursor = cursor[part]
        return cursor

    def node_exists(self, path_parts):
        if not path_parts:
            return True
        return self.get_node(path_parts) is not None

    def is_directory(self, path_parts):
        if not path_parts:
            return True
        node = self.get_node(path_parts)
        return isinstance(node, dict)

def _read_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, "rb") as file:
            return file.read().hex()

def _build_tree(physical_dir):
    tree = {}
    with os.scandir(physical_dir) as entries:
        for entry in entries:
            if entry.is_dir(follow_symlinks=False):
                tree[entry.name] = _build_tree(entry.path)
            elif entry.is_file(follow_symlinks=False):
                tree[entry.name] = _read_file_content(entry.path)
    return tree

def load_vfs_from_directory(dir_path):
    if not os.path.exists(dir_path):
        return None, f"VFS error: directory '{dir_path}' does not exist"
    if not os.path.isdir(dir_path):
        return None, f"VFS error: path '{dir_path}' is not a directory"
    root_name = os.path.basename(os.path.abspath(dir_path))
    vfs = VFS(root_name)
    try:
        vfs.root = _build_tree(dir_path)
        return vfs, None
    except OSError as err:
        return None, f"VFS error: failed to read directory: {err}"