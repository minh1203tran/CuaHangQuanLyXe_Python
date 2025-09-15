class VehicleView:
    @staticmethod
    def show_list(vehicles):
        if not vehicles:
            print("Không tìm thấy xe nào khớp với điều kiện!")
            return

        print("\n--- DANH SÁCH XE ---")
        for v in vehicles:
            print(f"ID: {v[0]} | Biển số: {v[1]} | Mẫu: {v[2]} | Hãng: {v[3]} | Năm: {v[4]}")

    @staticmethod
    def show_detail(vehicle):
        if vehicle:
            print("\n--- THÔNG TIN XE ---")
            print(f"ID: {vehicle[0]}")
            print(f"Biển số: {vehicle[1]}")
            print(f"Mẫu: {vehicle[2]}")
            print(f"Hãng: {vehicle[3]}")
            print(f"Năm: {vehicle[4]}")
        else:
            print("Không tìm thấy xe.")

    @staticmethod
    def show_message(msg):
        print(f"{msg}")

    @staticmethod
    def show_error(err):
        print(f"[ERROR] {err}")