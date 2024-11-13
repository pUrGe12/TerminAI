#!/usr/bin/env python3

import os
import json
from pathlib import Path
from typing import Dict, List, Any

class DirectoryParser:
    def __init__(self, output_file: str = "directory_structure.json"):
        self.output_file = output_file
        self.home_dir = str(Path.home())

    def _parse_directory(self, path: str, max_depth: int, current_depth: int = 0) -> List[Dict[str, Any]]:
        """
        Recursively parse a directory up to max_depth.
        Includes full path information for each file.
        """
        results = []
        try:
            if max_depth != -1 and current_depth > max_depth:
                return results

            with os.scandir(path) as entries:
                for entry in entries:
                    entry_info = {
                        "name": entry.name,
                        "type": "directory" if entry.is_dir() else "file",
                        "full_path": str(Path(entry.path).absolute())
                    }

                    if entry.is_dir():
                        try:
                            contents = self._parse_directory(
                                entry.path, 
                                max_depth, 
                                current_depth + 1
                            )
                            if contents:
                                entry_info["contents"] = contents
                        except PermissionError:
                            continue

                    results.append(entry_info)

        except PermissionError:
            print(f"Permission denied for {path}")
        except Exception as e:
            print(f"Error processing {path}: {str(e)}")

        return sorted(results, key=lambda x: (x["type"] == "file", x["name"]))

    def parse(self) -> None:
        """Parse the directory structure and save to JSON file."""
        print("Parsing directories...")
        
        # Create structure with paths
        directory_structure = {
            "root": self._parse_directory("/", max_depth=0),
            "home": {
                "desktop": self._parse_directory(os.path.join(self.home_dir, "Desktop"), max_depth=3),
                "downloads": self._parse_directory(os.path.join(self.home_dir, "Downloads"), max_depth=3),
                "documents": self._parse_directory(os.path.join(self.home_dir, "Documents"), max_depth=3)
            }
        }

        # Save to JSON file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(directory_structure, f, indent=2, ensure_ascii=False)
        
        print(f"Directory structure saved to: {self.output_file}")

if __name__ == "__main__":
    parser = DirectoryParser()
    parser.parse()