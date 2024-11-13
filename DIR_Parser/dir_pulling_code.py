#!/usr/bin/env python3

import json
import os
from typing import Optional, Tuple, List
from directory_parser import DirectoryParser

parser = DirectoryParser()
parser.parse()

class FileFinder:
    def __init__(self, json_file: str = "directory_structure.json"):
        self.json_file = json_file
        self.directory_data = self._load_json()

    def _load_json(self) -> dict:
        """Load the directory structure from JSON file."""
        try:
            with open(self.json_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"Directory structure file '{self.json_file}' not found.")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON in '{self.json_file}'.")

    def _search_in_data(self, data: List[dict], filename: str) -> Optional[str]:
        """Recursively search for a file in the directory data."""
        for item in data:
            # Check if current item is the file we're looking for
            if item['type'] == 'file' and item['name'] == filename:
                return item.get('full_path')
            
            # If it's a directory, search its contents
            if item['type'] == 'directory' and 'contents' in item:
                result = self._search_in_data(item['contents'], filename)
                if result:
                    return result
        return None

    def find_file(self, filename: str, location: Optional[str] = None) -> Optional[str]:
        """
        Find a file in the directory structure.
        Args:
            filename: Name of the file to find
            location: Specific location to search (desktop, downloads, documents, root)
        Returns:
            Full path of the file if found, None otherwise
        """
        # If location is specified, search only that location
        if location:
            location = location.lower()
            if location == 'root':
                return self._search_in_data(self.directory_data['root'], filename)
            elif location in ['desktop', 'downloads', 'documents']:
                return self._search_in_data(self.directory_data['home'][location], filename)
            else:
                raise ValueError(f"Invalid location: {location}")

        # If no location specified, search everywhere
        # First search root
        path = self._search_in_data(self.directory_data['root'], filename)
        if path:
            return path

        # Then search home directories
        for location in ['desktop', 'downloads', 'documents']:
            path = self._search_in_data(self.directory_data['home'][location], filename)
            if path:
                return path

        return None

    def open_file(self, filename: str, location: Optional[str] = None) -> Tuple[bool, str]:
        """
        Find and open a file.
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            file_path = self.find_file(filename, location)
            if not file_path:
                return False, f"File '{filename}' not found"

            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                return True, content
            except Exception as e:
                return False, f"Error opening file: {str(e)}"

        except Exception as e:
            return False, f"Error: {str(e)}"

def main():
    # Example usage
    finder = FileFinder()

    # Example 2: Find and open a file anywhere
    success, result = finder.open_file("api_keys.py")
    if success:
        print("File content:")
        print(result)
    else:
        print("Error:", result)

if __name__ == "__main__":
    main()