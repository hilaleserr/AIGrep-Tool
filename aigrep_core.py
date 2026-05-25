import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def process_file(file_path, search_pattern, replace_text=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        results = []
        for i, line in enumerate(lines):
            if re.search(search_pattern, line):
                results.append({"file": str(file_path), "line_number": i + 1, "original_content": line.strip()})
        return results
    except:
        return []

def arama_yap(pattern, search_path, replace_text=None, ext_list=['.py']):
    path_obj = Path(search_path)
    files_to_process = []
    if path_obj.is_dir():
        for root, _, files in os.walk(path_obj):
            for file in files:
                if any(file.endswith(ext) for ext in ext_list):
                    files_to_process.append(Path(root) / file)
    
    all_results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, f, pattern, replace_text) for f in files_to_process]
        for future in futures:
            res = future.result()
            if res: all_results.extend(res)
    return all_results