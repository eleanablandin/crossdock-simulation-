"""
Reporting utilities for the crossdock simulation.

This module provides helper functions to export:
- item logs (from Scanner)
- row status (from Truck.rows_status())
- truck summary (from Truck.summary())

All exports use CSV format so they can be easily analyzed later with tools
like Excel or pandas.
"""


import csv 
from pathlib import Path 
from typing import List, Dict, Any 

def ensure_directory(path: str | Path) -> Path: 

    """

    Ensure the parent directory of a file path exists.
    Returns the Path object for the file.

    """

    path = Path(path)
    parent = path.parent

    if parent and not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)
    return path 

def export_item_logs_csv(item_logs: List[Dict[str, Any]], filepath: str | Path) -> None :

    """
    Export scanner item logs to a CSV file.

    Args:
        item_logs: List of dicts, typically Scanner.item_logs.
        filepath: Target CSV file path (e.g., 'reports/item_logs.csv').
    """
    

    if not item_logs:
        #   Nothing to export
        return
    
    filepath = ensure_directory(filepath)
    
    # Use keys of the first log as CSV headers 
    fieldnames = list(item_logs[0].keys())

    with filepath.open(mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(item_logs)


def export_rows_status_csv(rows_status: List[Dict[str, any]], filepath: str | Path) -> None:

    """
    Export truck row status to CSV.

    Args:
        rows_status: List of dicts from Truck.rows_status().
        filepath: Target CSV file path.
    """

    if not rows_status:
        return 
    
    filepath = ensure_directory(filepath)
    fieldnames = list(rows_status[0].keys())

    with filepath.open(mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_status)

def export_truck_summary_csv(summary: List[Dict[str, any]], filepath: str | Path) -> None:

    """
    Export a single truck summary as a one-row CSV.

    Args:
        summary: Dict returned by Truck.summary().
        filepath: Target CSV file path.
    """

    if not summary:
        return 
    
    filepath = ensure_directory(filepath)
    fileldnames = list(summary.keys())

    with filepath.open(mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fileldnames)
        writer.writeheader()
        writer.writerow(summary)