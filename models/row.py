

class Row:
    def __init__(self, row_id:int, items: list):
        self.row_id = row_id
        self.items = items
        self.strap_needed = 1
    
    def is_valid(self) -> bool:

        pass

    def row_type(self) -> str:
        pass