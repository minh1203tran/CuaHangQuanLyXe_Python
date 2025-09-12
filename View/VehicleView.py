class VehicleView:
    @staticmethod
    def show_list(vehicles):
        print("\n--- DANH SÁCH XE ---")
        for v in vehicles:
            print(f"ID: {v[0]} | Biển số: {v[1]} | Mẫu: {v[2]} | Hãng: {v[3]} | Năm: {v[4]}")

    @staticmethod
    def show_message(msg):
        print(f"[INFO] {msg}")
