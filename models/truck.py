from typing import List, Optional, Dict, Any 
from models.row import Row


class Truck:

    def __init__(self, truck_id: str, door: Optional[str] = None, strap_reach_limit: int =3):

        self.truck_id = truck_id
        self.door = door 
        self.rows: List[Row] = []
        self.strap_reach_limit = strap_reach_limit
        
    def add_row(self, row: Row):
        self.rows.append(row)
    
    def total_rows(self) -> int:
        return len(self.rows)
    
    def valid_rows(self) -> List[Row]:
        return [r for r in self.rows if r.is_valid()]
    
    def is_row_reachable(self, row_index: int) -> bool:
        return row_index <= self.strap_reach_limit
    
    def straps_required(self) -> int:

        """
        Required straps = number of valid rows.
        Valid rows are rows of:
          - 2 pallets
          - 3 cars
       """
        # return sum(1 for r in self.rows if r.is_valid())
        return sum(row.required_straps() for row in self.rows)
    
    def straps_applied(self) -> int:

        """
        Returns the number of straps applied across all rows.
        A strap is applied only if:
         - the row is valid (2 pallets or 3 cars)
         - the row is reachable by strap (self.is_row_reachable)
        """

        applied = 0 

        for i, row in enumerate(self.rows, start=1):
            if row.is_valid() and self.is_row_reachable(i):
                applied += 1
        return applied
    
    def rows_status(self) -> List[Dict[str, Any]]:

        status_list = []

        for i, row in enumerate(self.rows, start=1):
            if not row.is_valid():
                status = "invalid"
                reason = "row does not meet rule (2 Pallets or 3 Cars)"
            elif self.is_row_reachable(i):
                status = "applied"
                reason = ""
            else:
                status = "not_possible_reach"
                reason = "beyond strap reach limit"
            
            status_list.append({
                "truck_id": self.truck_id,
                "door": self.door,
                "row_id": row.row_id,
                "row_type": row.row_type(),
                "strap_required": 1 if row.is_valid() else 0,
                "strap_status": status,
                "reason": reason 
                                        
            })
        return status_list
    
    def summary(self) -> Dict[str, Any]:

        total = self.total_rows()
        valid = len(self.valid_rows())
        required = self.straps_required()
        applied = self.straps_applied()
        unreachable = max(0, required - applied)

        return {
            "truck_id": self.truck_id,
            "door": self.door,
            "total_rows": total,
            "valid_rows": valid,
            "straps_required": required,
            "straps_applied": applied,
            "straps_unreachable": unreachable,
            "safety_index_pct": round(100.0 * applied / required, 2) if required > 0 else 0.0
        }
