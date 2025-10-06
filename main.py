from models.row import Row
from models.item import Pallet, Car
from models.truck import Truck

# def test_rows():
#     """Prueba rápida de filas con pallets y cars"""
#     row1 = Row(1, [Pallet("1-01"), Pallet("1-02")])          # válido: 2 pallets
#     row2 = Row(2, [Car("2-01"), Car("2-02"), Car("2-03")])   # válido: 3 cars
#     row3 = Row(3, [Pallet("3-01"), Car("3-02")])             # inválido: mezcla

#     for r in [row1, row2, row3]:
#         print(f"Row {r.row_id}: {r.row_type()}, "
#               f"Valida? {r.is_valid()}, "
#               f"Straps: {r.strap_needed}")

# if __name__ == "__main__":
#     print("=== Prueba de Rows ===")
#     test_rows()

def main():
    # --- Crear filas ---
    row1 = Row(1, [Pallet("1-01"), Pallet("1-02")])  # válida
    row2 = Row(2, [Car("2-01"), Car("2-02"), Car("2-03")])  # válida
    row3 = Row(3, [Pallet("3-01"), Car("3-02")])  # inválida
    row4 = Row(4, [Car("4-01"), Car("4-02"), Car("4-03")])  # válida
    row5 = Row(5, [Pallet("5-01"), Pallet("5-02")])  # válida

    # --- Crear camión ---
    truck = Truck(truck_id="TRK-001", door="DOOR-07", strap_reach_limit=3)

    # --- Agregar filas ---
    for r in [row1, row2, row3, row4, row5]:
        truck.add_row(r)


    truck2 = Truck(truck_id="TRK-002", door="DOOR-12", strap_reach_limit=2)

    row2_1 = Row(1, [Car("2-01"), Car("2-02"), Car("2-03")])   # válida
    row2_2 = Row(2, [Car("2-04"), Car("2-05"), Car("2-06")])   # válida
    row2_3 = Row(3, [Pallet("2-07"), Pallet("2-08")])          # válida pero fuera de alcance
    for r in [row2_1, row2_2, row2_3]:
        truck2.add_row(r)

    print("=== CAMIÓN 1 ===")
    for status in truck.rows_status():
        print(status)
    print("Resumen:", truck.summary())

    print("\n=== CAMIÓN 2 ===")
    for status in truck2.rows_status():
        print(status)
    print("Resumen:", truck2.summary())


if __name__ == "__main__":
    main()