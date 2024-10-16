import os
import sys

import base64
import pickle

import paramiko

def get_executable_directory():
    if getattr(sys, 'frozen', False):
        executable_directory = os.path.dirname(sys.executable)
    else:
        executable_directory = os.path.dirname(os.path.abspath(__file__))

    return executable_directory

def list_directories(path):
    all_entries = os.listdir(path)
    directories = [entry for entry in all_entries if os.path.isdir(os.path.join(path, entry))]

    return directories

def list_files_in_directory(path):
    files = [os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]

    return files

class TREE_NODE:
    def __init__(self, filepath):
        self.children = []
        self.filepath = filepath
        self.video = self.load_and_encode_video(filepath)

    def load_and_encode_video(self, filepath):
        if not os.path.isfile(filepath):
            return None 

        try:
            with open(filepath, 'rb') as file:
                binary_content = file.read()

                return base64.b64encode(binary_content).decode('utf-8')

        except Exception as e:
            print(f"Error loading video file {filepath}: {e}")
            
            return None
    
    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return self.filepath

class TREE:
    def __init__(self):
        _dir = get_executable_directory()
        self.head = TREE_NODE(_dir)
        _dir_list = list_directories(_dir)
        
        for item in _dir_list:
            full_path = os.path.join(_dir, item)
            dir_node = TREE_NODE(full_path)
            self.head.add_child(dir_node)

            if os.path.isdir(full_path):
                file_list = list_files_in_directory(full_path)
                for filey in file_list:
                    file_node = TREE_NODE(filey)
                    dir_node.add_child(file_node)

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.head
        
        print(" " * (level * 4) + "|-- " + os.path.basename(node.filepath))
        
        for child in node.children:
            self.print_tree(child, level + 1)

    def pickle_tree(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        print(f"Tree pickled to {filename}")

    @staticmethod
    def unpickle_tree(filename):
        with open(filename, 'rb') as f:
            tree = pickle.load(f)
        print(f"Tree unpickled from {filename}")
        return tree