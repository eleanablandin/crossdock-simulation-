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


row1 = Row(1, [Pallet("1-01"), Pallet("1-02")])  # 2 pallets
row2 = Row(2, [Car("2-01"), Car("2-02"), Car("2-03")])  # 3 cars

# Creamos fila inválida (mezclada)
row3 = Row(3, [Pallet("3-01"), Car("3-02")])

print("Row1:", row1.row_type(), "Valida?", row1.is_valid(), "Straps:", row1.strap_needed)
print("Row2:", row2.row_type(), "Valida?", row2.is_valid(), "Straps:", row2.strap_needed)
print("Row3:", row3.row_type(), "Valida?", row3.is_valid(), "Straps:", row3.strap_needed)