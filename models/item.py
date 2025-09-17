"""
item.py 

This module define classes for scannable items in a crossdock simulation. 
Each item(e.g., pallet, car) has attributes such as:

- a unique ID

- whether its barcode is valid 

- whether its label is damaged 

- its assigned destination 

The module also provides methods to check if an items is scannable
and convert its attributes into a dictionary.


"""

from collections import Counter
import random

class ItemBase:


    def __init__(self, id_str: str, item_type:str):

        """
        Initialize a new item.

        Args:
            id_str (str): Identifier string for the item.
            item_type (str): Type of the item (e.g., 'PALLET', 'CAR').
        
        """
        self.id = f"{item_type}-{id_str}"
        self.type = item_type
        self.barcode_valid = random.random() > 0.05 # ~95% chance barcode is valid 
        self.label_damaged = random.random() < 0.08 # ~8% chance label is damaged 
        self.destination = random.choice(["BAY-A", "BAY-B", "BAY-C", "BAY-D"])
    
    def to_dict(self):

        """
        Convert the item attributes into a dictionary.

        Returns:
            dict: A dictionary containing item details.
        
        """

        return {
            "id": self.id,
            "type": self.type,
            "barcode_valid": self.barcode_valid,
            "label_dameged": self.label_damaged,
            "destination": self.destination
        }
    
    def is_scannable(self) -> bool:

        """
        Determine if the item is scannable.

        An item is considered scannable if its barcode is valid
        and its label is not damaged.

        Returns:
            bool: True if the item can be scanned, False otherwise.
        
        """
        return self.barcode_valid and not self.label_damaged
    
class Pallet(ItemBase):
    def __init__(self, id_str):
        super().__init__(id_str, "PALLET")

class Car(ItemBase):
    def __init__(self, id_str):
        super().__init__(id_str, "CAR")

## QUICK TEST  ## 
items = [Pallet(f"P-{i:02d}") for i in range(1, 11)] + \
        [Car(f"C-{i:02d}") for i in range(1, 11)]

# Count how many items are scannable
results = [item.is_scannable() for item in items]

count = Counter(results)

print("Resultados de escaneabilidad:")
print(f"Escaneables (True): {count[True]}")
print(f"No escaneables (False): {count[False]}")

# Show details of the first 5 items
print("\nDetalle de algunos items:")
for item in items[:5]:
    print(item.to_dict(), "=> is_scannable:", item.is_scannable())