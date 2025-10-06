from models.item import Pallet, Car

class Row:
    def __init__(self, row_id:int, items: list):
        self.row_id = row_id
        self.items = items
        self.strap_needed = 1
    
    def is_valid(self) -> bool:
        
        if len(self.items) == 2 and all(isinstance(i, Pallet) for i in self.items):
            return True 
        
        if len(self.items) == 3 and all(isinstance(i, Car) for i in self.items):
           return True 
        
        return False 
    
    def row_type(self) -> str:

        if self.is_valid():
            return self.items[0].type
        return "Invalid"
