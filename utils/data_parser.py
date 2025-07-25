import json
import csv
from typing import List, Dict, Union

def parse_csv(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, mode="r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def parse_json(file_path: str) -> Union[Dict, List[Dict]]:
    with open(file_path, mode="r", encoding="utf-8") as f:
        return json.load(f)

def parse_data(file_path: str) -> Union[Dict, List[Dict]]:
    if file_path.endswith(".csv"):
        return parse_csv(file_path)
    elif file_path.endswith(".json"):
        return parse_json(file_path)
    else:
        raise ValueError("Unsupported file format. Only CSV and JSON are supported.")
