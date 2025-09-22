class VehicleView:
    @staticmethod
    def show_list(vehicles):
        if not vehicles:
            print("--- Không có dữ liệu xe ---")
            return
        print("--- Danh Sách Xe ---")
        for v in vehicles:
            print(f"ID: {v[0]} | Biển số: {v[1]} | Dòng: {v[2]} | Hãng: {v[3]} | "
                  f"Năm: {v[4]} | Ngày tạo: {v[5]} | Giá: {v[6]:,} VNĐ")

    @staticmethod
    def show_detail(vehicle):
        if vehicle and len(vehicle) > 0:
            vehicle_data = vehicle[0] if isinstance(vehicle, list) else vehicle
            print("--- THÔNG TIN XE ---")
            print(f"ID: {vehicle_data[0]}")
            print(f"Biển số: {vehicle_data[1]}")
            print(f"Mẫu: {vehicle_data[2]}")
            print(f"Hãng: {vehicle_data[3]}")
            print(f"Năm: {vehicle_data[4]}")
            print(f"Ngày tạo: {vehicle_data[5]}")
            print(f"Giá: {vehicle_data[6]:,} VNĐ")
        else:
            print("Không tìm thấy xe.")

    @staticmethod
    def show_message(msg):
        print(f"{msg}")

    @staticmethod
    def show_error(err):
        print(f"[ERROR] {err}")