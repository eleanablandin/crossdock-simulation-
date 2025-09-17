from models.row import Row
from models.item import Pallet, Car

def test_rows():
    """Prueba rápida de filas con pallets y cars"""
    row1 = Row(1, [Pallet("1-01"), Pallet("1-02")])          # válido: 2 pallets
    row2 = Row(2, [Car("2-01"), Car("2-02"), Car("2-03")])   # válido: 3 cars
    row3 = Row(3, [Pallet("3-01"), Car("3-02")])             # inválido: mezcla

    for r in [row1, row2, row3]:
        print(f"Row {r.row_id}: {r.row_type()}, "
              f"Valida? {r.is_valid()}, "
              f"Straps: {r.strap_needed}")

if __name__ == "__main__":
    print("=== Prueba de Rows ===")
    test_rows()