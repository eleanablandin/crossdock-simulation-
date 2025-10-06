from __future__ import annotations
from typing import List, Dict, Any, Optional
import random
from datetime import datetime

from models.item import ItemBase, Pallet, Car
from models.row import Row
from models.truck import Truck

class Scanner:
    """
    Responsibilities:
    - Scan individual items (Cars or Pallets) via barcode.
    - Confirm item placement using QR codes located at truck doors (IN = wall, OUT = floor).
    - Automatically group scanned items into valid Rows inside the assigned Truck.
    - Keep detailed logs for every scanned item and every created Row.
    - Generate performance metrics (KPIs) such as success rate, time, and attempts.

    Rules:
    - Two Pallets = one valid Row
    - Three Cars = one valid Row
    - Mixed Rows (Cars + Pallets) are invalid and not created by this class.
    """

    def __init__(
            self,
            name: str = "Scanner-01",
            base_success: float = 0.98,
            mean_time_s: float = 2.8,
            max_attempts: int = 3,
            door_fail_rate: float = 0.001
                 ):
        """
        Initialize a Scanner instance.

        Args:
            name (str): Operator name or device ID.
            base_success (float): Base probability of a successful barcode scan (if label is intact).
            mean_time_s (float): Average time (in seconds) for the first scan attempt.
            max_attempts (int): Maximum number of scan retries per item.
            door_fail_rate (float): Probability that a QR code scan (IN/OUT) fails.


        """
        
        
        self.name = name
        self.base_success = base_success
        self.mean_time_s = mean_time_s
        self.max_attempts = max_attempts
        self.door_fail_rate = door_fail_rate

        # structure: { truck_id: {"Pallet": [items...], "Car": [items...] } }
        self.buffers: Dict[str, Dict[str, List[ItemBase]]] = {}

        # Logs for detailed tracking
        self.item_logs: List[Dict[str, Any]] = []
        self.row_logs: List[Dict[str, Any]] = []

    # -------------------------------------------------------------------------
    # SCAN PROCESS
    # -------------------------------------------------------------------------
    def _scan_once(self, item: ItemBase) -> bool:
        """

        Perform a single scan attempt for an item.
        Adjust success probability based on barcode and label conditions.

        Returns:
            bool: True if scan succeeds, False otherwise.

        """

        if not item.barcode_valid:
            success_prob = 0.12
        elif item.label_damaged:
            success_prob = self.base_success * 0.6
        else:
            success_prob = self.base_success
        return random.random() < success_prob
                 
        
    def scan_item(self, item: ItemBase) -> Dict[str, Any]:

        """
        Attempt to scan a single item up to 'max_attempts' times.

        The first attempt takes longer on average (mean_time_s),
        while subsequent attempts are faster (~1.4s mean).

        Returns:
            dict: {
                "success": bool,
                "attempts": int,
                "time_s": float
            }
        """

        attempts = 0 
        success = False
        total_time = 0.0 

        while attempts < self.max_attempts and not success:
            attempts += 1

            # Time for each attempt (Gaussian noise for realism)
            mu = self.mean_time_s if attempts == 1 else 1.4
            sigma = 0.5
            t = max(0.4, random.gauss(mu, sigma))
            total_time += t 

            success  = self._scan_once(item)
            
        return {
            "success": success,
            "attempts": attempts,
            "time_s": round(total_time, 2)
            }
    
    # -------------------------------------------------------------------------
    # QR CONFIRMATION SCANS
    # -------------------------------------------------------------------------
    def scan_door_in(self, truck: Truck) -> bool:

        """
        Simulate scanning the QR code on the wall (item enters truck).

        Returns:
            bool: True if QR IN scan succeeds, False otherwise.
        """
        success_prob = 0.9954
        return random.random() < success_prob
    
    def scan_door_out(self, truck:Truck) -> bool:
        
        """
        Simulate scanning the QR code on the floor (item exits truck).

        Returns:
            bool: True if QR OUT scan succeeds, False otherwise.
        """
        
        success_prob = 0.995
        return random.random() < success_prob
    

    # -------------------------------------------------------------------------
    # BUFFER & ROW HANDLING
    # -------------------------------------------------------------------------
    def _ensure_buffers(self, truck: Truck) -> None:
        """Ensure buffer structure exists for the given truck."""
        if truck.truck_id not in self.buffers:
            self.buffers[truck.truck_id] = {"Pallet": [], "Car":[]}
    
    def _flush_if_full(self, truck: Truck, item_type: str) -> Optional[Row]:

        """
        Check if the buffer for a given item type (Pallet/Car) is full enough
        to form a valid Row. If so, create and add the Row to the Truck.

        Returns:
            Row | None: Newly created Row if buffer was full, otherwise None.
        """
        buf = self.buffers[truck.truck_id][item_type]
        needed = 2 if item_type == "Pallet" else 3

        if len(buf) >= needed:
            # Remove exactly the items that complete a row
            items_for_row = [buf.pop(0) for _ in range(needed)]
            row_id = len(truck.rows) + 1
            row = Row(row_id, items_for_row)
            truck.add_row(row)

            # Log row creation
            self.row_logs.append({
                "timestamp": datetime.now(),
                "scanner": self.name,
                "truck_id": truck.truck_id,
                "door": truck.door,
                "row_type": row.row_type(),
                "items_count": len(items_for_row)
            })
            return row
        return None 
    
    # -------------------------------------------------------------------------
    # MAIN PROCESS FLOW
    # -------------------------------------------------------------------------
    def process_batch(self, items: List[ItemBase], truck: Truck) -> None:
        """
        This function process a items list for a truck (assigned for a PA). 
        For every item: scann, confirm at door and push it to the corresponding buffer.
        When the buffer is full, it creates a row.

        """
        """
        Process a batch of items assigned to a specific truck.
        Each item follows the realistic scanning sequence:
            1. Scan barcode
            2. Confirm at truck door (QR IN)
            3. Add to buffer and create Row if buffer is full

        Args:
            items (List[ItemBase]): Items to be processed.
            truck (Truck): Destination truck.
        """

        self._ensure_buffers(truck)

        for item in items:

            res = self.scan_item(item) # Step 1: barcode scan

             # Step 2: confirm with QR IN (wall)
            if res["success"]:
                door_in_ok = self.scan_door_in(truck)
            else:
                door_in_ok = False 
            
            door_out_ok = None  # future use (for removals)
            new_row_id = None 

            # Step 3: push to buffer and create Row if full
            if door_in_ok:
                if item.type not in ("Pallet", "Car"):
                    pass
                else:
                    self.buffers[truck.truck_id][item.type].append(item)
                    created = self._flush_if_full(truck, item.type)
                    if created is not None:
                        new_row_id = created.row_id

            
            # Step 4: log everything
            self.item_logs.append({
                "scanner": self.name,
                "truck_id": truck.truck_id,
                "door": truck.door,
                "item_id": item.id,
                "item_type": item.type,
                "barcode_valid": item.barcode_valid,
                "label_damaged": item.label_damaged,
                "scan_success": res["success"],
                "attempts": res["attempts"],
                "scan_time_s": res["time_s"],
                "door_in_ok": door_in_ok,
                "door_out_ok": door_out_ok,
                "row_created_id": new_row_id
            })


    # -------------------------------------------------------------------------
    # TRUCK CLOSING
    # -------------------------------------------------------------------------
    def close_truck(self, truck: Truck, finalize_incomplete_rows: bool = False) -> None:
    
        """
        Clear or finalize buffers when a truck is ready to depart (TDR OUT).

        Args:
            truck (Truck): The truck being closed.
            finalize_incomplete_rows (bool): 
                - If False → drop incomplete buffers (default behavior).
                - If True → push incomplete items as invalid rows (forced close).
        """

        self._ensure_buffers(truck)
        if not finalize_incomplete_rows:
            self.buffers[truck.truck_id]["Pallet"].clear()
            self.buffers[truck.truck_id]["Car"].clear()
            return 
        
        # Force incomplete rows (e.g., TDR OUT due to time)
        for type in ("Pallet", "Car"):
            buf = self.buffers[truck.truck_id][type]
            if len(buf) > 0:
                row_id = len(truck.rows) + 1
                row = Row(row_id, list(buf))
                truck.add_row(row)
                self.row_logs.append({
                    "timestamp": datetime.now(),
                    "scanner": self.name,
                    "truck_id": truck.truck_id,
                    "door": truck.door,
                    "row_id": row_id,
                    "row_type": row.row_type(),
                    "items_count": len(buf),
                    "note": "forced close; may be invalid"
                    
                })
                buf.clear()

    # -------------------------------------------------------------------------
    # METRICS
    # -------------------------------------------------------------------------
    def metrics(self) -> Dict[str, Any]:
        """
        KPIs
        """
        """
        Compute scanner performance metrics (KPIs) for this session.

        Returns:
            dict: {
                "scanner": str,
                "items_processed": int,
                "scan_success_pct": float,
                "door_scan_ok_pct": float,
                "avg_scan_time_s": float,
                "avg_attempts": float
            }
        """

        if not self.item_logs:
            return {
                "scanner": self.name, 
                "items_processed": 0,
                "scan_success_pct": 0.0, 
                "door_scan_ok_pct": 0.0,
                "avg_scan_time_s": 0.0,
                "avg_attempts": 0.0
            }
        
        n = len(self.item_logs)
        succ = sum(1 for x in self.item_logs if x["scan_success"])
        door_ok = sum(1 for x in self.item_logs if x["door_in_ok"])
        avg_t = sum(x["scan_time_s"] for x in self.item_logs) / n
        avg_a = sum(x["attempts"] for x in self.item_logs) / n 

        return {
            "scanner": self.name,
            "items_processed": n,
            "scan_success_pct": round(100.0 * succ / n, 2),
            "door_scan_ok_pct": round( 100.0 * door_ok / n, 2),
            "avg_scan_time_s": round(avg_t, 2),
            "avg_attempts": round(avg_a, 2)
        }