from models.item import Pallet, Car

class Row:

    """
    Represents a row inside a truck.
    A row is valid ONLY if:
      - it has 2 Pallets, OR
      - it has 3 Cars
    """

    def __init__(self, row_id:int, items: list):
        self.row_id = row_id
        self.items = items
    
    def is_valid(self) -> bool:
        """Check if row follows crossdock rules."""
        
        # Rule: 2 pallets
        if len(self.items) == 2 and all(isinstance(i, Pallet) for i in self.items):
            return True 
        
        # Rule: 3 cars
        if len(self.items) == 3 and all(isinstance(i, Car) for i in self.items):
           return True 
        
        return False 
    
    def row_type(self) -> str:
        """Return 'Pallet', 'Car', or 'Invalid'."""
        if self.is_valid():
            return self.items[0].type
        return "Invalid"
    
    def required_straps(self) -> int:
        """Each valid row requires 1 strap."""
        return 1 if self.is_valid() else 0 
    
    
